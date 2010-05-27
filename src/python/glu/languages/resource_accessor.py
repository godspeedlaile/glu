
from glu.resources.resource_runner    import accessResource
from org.mulesource.glu.component.api import HttpResult

from org.mulesource.glu               import ResourceAccessorInterface

class ResourceAccessor(ResourceAccessorInterface):
    """
    This is a helper class that we use to give the Java base component
    access to our accessResource() method.
    
    When a Java component is invoked, it receives an instance
    of this class here, which provides painless access to the
    Python method.
    
    """
    def __init__(self, from_java_conversion_func, to_java_conversion_func):
        """
        Caller provides us with a pre-initialized function to convert
        Java 'dict' objects to Python.
        
        """
        self.from_java_conversion_func = from_java_conversion_func
        self.to_java_conversion_func   = to_java_conversion_func
        
    def accessResourceProxy(self, uri, input, params, method):
        res = HttpResult()
        res.status, res.data = accessResource(uri, input, self.from_java_conversion_func(params), method)
        res.data = self.to_java_conversion_func(res.data)
        return res