
"""
This module takes care of the translation of language
specific data structures and types into the types that
are used in the Python core.

You may wonder why this functionality is not simply integrated
in the base component class for each language. Turns out that
such conversion is much simpler in Python than in (for example)
Java. Therefore, we put this conversion outside of the base
component.

The tradeof is that we need to make sure to call the proper
conversion function whenever we use the components.

"""

from glu.platform_specifics           import PLATFORM, PLATFORM_JYTHON

from org.mulesource.glu.exception     import *
from org.mulesource.glu.component.api import HTTP, HttpMethod, Result

if PLATFORM == PLATFORM_JYTHON:
    import java.lang.Exception
    from java.lang import String, Integer, Float
    from java.math import BigDecimal
    from java.util import HashMap, ArrayList


def __javaStructToPython(hm):
    """
    Convert a Java HashMap and ArrayList based structure to a Python dictionary or list.
    
    Sadly, this is not done automatically. So, we recursively
    iterate over the hash map and convert using the 'update' method
    of dictionaries. Unfortunately, 'update' only works on the same
    level and doesn't do the conversion recursively.
    
    """
    if type(hm) is HashMap:
        d2 = dict()
        d2.update(hm)
        for key, val in d2.items():
            if type(val) in [ HashMap, ArrayList ]:
                d2[key] = __javaStructToPython(val)
            else:
                # If it's one of those Java numeric types then we need to
                # forcefully convert it to a Python numeric type, since
                # otherwise JSON gets confused and exports the value as
                # a string.
                if type(val) in [ Integer, Float, BigDecimal ]:
                    d2[key] = float(val.toString())

    elif type(hm) is ArrayList:
        d2 = list()
        for val in hm:
            if type(val) in [ HashMap, ArrayList ]:
                d2.append(__javaStructToPython(val))
            else:
                d2.append(val)
    else:
        return hm
            
    return d2


def __pythonStructToPython(obj):
    """
    Nothing needs to be done for Python.
    
    """
    return obj

def __pythonStructToJava(obj):
    """
    Traverse dicts and lists and convert to Java HashMaps
    and ArrayLists.
    
    """
    if type(obj) is dict:
        elem = HashMap()
        for key, value in obj.items():
            elem.put(key, __pythonStructToJava(value))
    elif type(obj) is list:
        elem = ArrayList()
        for e in obj:
            elem.add(__pythonStructToJava(e))
    else:
        elem = obj
    return elem

#
# Translation table, which finds the correct conversion function
# based on the language ID of the component.
#
__LANG_STRUCT_TO_PYTHON = {
   "JAVA"   : __javaStructToPython,
   "PYTHON" : __pythonStructToPython
}


def languageStructToPython(component, obj):
    """
    Convert a struct of the component's language to a Python equivalent.
    
    Chooses the correct conversion function for this component, based
    on the language ID that's returned by the component.
    
    """
    func = __LANG_STRUCT_TO_PYTHON[component.LANGUAGE]
    return func(obj)


#
# Proxies for calling language specific component service methods
#
def __javaServiceMethodProxy(component, request, method, method_name, input, params, http_method):
    """
    Calls service methods in Java components.
    
    Prepares parameters, converts exceptions and results.
    
    """
    if request:
        request.setNativeMode()
    # We remove the resource creation time parameters from the map and
    # assign them directly to the component as new attributes. After that,
    # the pruned parameter map can be passed as keyword arg dict to the
    # service method.
    for name in component.componentDescriptor.getParamMap().keySet():
        if name in params:
            setattr(component, name, params[name])
            del params[name]
    try:
        param_order = component.getParameterOrder()[method_name]
        param_types = component.getParameterTypes()[method_name]
        # Assemble the list of additional service method parameters. We need
        # to perform a case, so we combine the type list and parameter name list,
        # index the parameter map and perform the cast all in one swoop.
        if param_order and param_types:
            # Yes, the following CAN be written as a single line with list comprehension,
            # but then the 'reader comprehension' suffers. So, I wrote it out explicitly.
            arglist = list()
            for param_type, name in zip(param_types, param_order):
                param_value = params[name]
                if param_type != type(param_value):
                    # Some type conversion is required
                    arglist.append(param_type(param_value))
                else:
                    # Type is already in the right argument (often the case when a default
                    # value was specified).
                    arglist.append(param_value)
        else:
            arglist = list()

        # Importing at this odd place here avoids circular imports in other places
        from resource_accessor import ResourceAccessor

        # Provide a conversion methods specific to this component's language.
        # Passing them to ResourceAccessor means that I don't have to import those
        # symbols in the resource_accessor module.        
        component.resourceAccessor = ResourceAccessor(__javaStructToPython, __pythonStructToJava)
        res = method(http_method, String(input if input is not None else ""), *arglist)
    except GluException, e:
        raise e
    except java.lang.Exception, e:
        print "Exception in component: ", e.printStackTrace()
        raise GluException(str(e))
    data = res.getEntity()
    if type(data) in [ HashMap, ArrayList ]:
        data = __javaStructToPython(data)
        res.setEntity(data)
    return res

def __pythonServiceMethodProxy(component, request, method, method_name, input, params, http_method):
    """
    Calls service methods in Python components.
    
    """
    # We remove the resource creation time parameters from the map and
    # assign them directly to the component as new attributes. After that,
    # the pruned parameter map can be passed as keyword arg dict to the
    # service method.
    for name in component.PARAM_DEFINITION.keys():
        if name in params:
            if hasattr(component, name):
                raise GluException("Name '%s' cannot be assigned to component, because an attribute with that name exists already" % name)
            setattr(component, name, params[name])
            del params[name]
    return method(http_method, input, **params)

#
# Translation table, which finds the correct conversion function
# based on the language ID of the component.
#
__LANG_METHOD_PROXIES = {
    "JAVA"   : __javaServiceMethodProxy,
    "PYTHON" : __pythonServiceMethodProxy,
}


def serviceMethodProxy(component, service_method, service_method_name, request, input, params, http_method):
    """
    Call the service method of a component.
    
    'component' is passed in only so that we can decide
    here, which proxy to use.

    'service_method' is not the name of the method, but a handle to
    the actual method itself already.

    'service_method_name' is the name of the method, as you
    might have guessed.
    
    """
    func = __LANG_METHOD_PROXIES[component.LANGUAGE]
    component.setRequest(request)
    return func(component, request, service_method, service_method_name, input, params, http_method)
