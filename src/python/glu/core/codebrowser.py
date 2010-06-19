"""
Allows users and clients to browse the server's installed code.

"""
# Java imports
import glujson as json

# Glu imports
import glu.settings as settings

from org.mulesource.glu.exception       import GluException
from org.mulesource.glu.component.api   import Result

from glu.components       import _CODE_MAP
from glu.resources        import makeResource 
from glu.core.basebrowser import BaseBrowser
from glu.languages        import *

from org.mulesource.glu.util          import Url
from org.mulesource.glu.component.api import HTTP;

EXCLUDE_PREFIXES = [ "_" ]

def getComponentClass(uri):
    """
    Return the specified component class, based on a given URI.
    
    @param uri:     The official URI for this code.
    @type uri:      string
    
    @return         Class of the specified component
                    or None if no matching component class was found.
    @rtype          A class derived from BaseComponent
    
    """
    path_elems = uri[len(settings.PREFIX_CODE):].split("/")[1:]
    component_name  = path_elems[0]   # This should be the name of the code element
    
    # Instantiate the component
    return _CODE_MAP.get(component_name)

def getComponentInstance(uri, resource_name = None):
    """
    Return an instantiated component, the class of which was identified by a URI.

    @param uri:           The official URI for this code.
    @type uri:            string

    @param resource_name: Name of the resource for which the component was instantiated.
    @type resource_name:  string
    
    @return               Instance of the specified component
                          or None if no matching component class was found.
    @rtype                Instance of a class derived from BaseComponent
    
    """
    component_class = getComponentClass(uri)
    if component_class:
        component = component_class()
        component.setResourceName(resource_name)
        return component
    else:
        return None
        
class CodeBrowser(BaseBrowser):
    """
    Handles requests for code info.
    
    """
    def __init__(self, request):
        """
        Initialize the browser with the render-args we need for meta data browsing.
        
        @param request: Handle to the HTTP request that needs to be processed.
        @type request:  GluHttpRequest
        
        """
        super(CodeBrowser, self).__init__(request,
                                          renderer_args = dict(no_annotations=True,
                                                               no_table_headers=False,
                                                               no_list_indices=False,
                                                               no_borders=False))
    
    def __process_get(self):
        """
        Respond to GET requests.
        
        When someone sends GET requests to the code then
        they want to browse the available code options.
        
        @return:  HTTP return structure.
        @rtype:   Result

        """
        # It's the responsibility of the browser class to provide breadcrumbs
        self.breadcrumbs = [ ("Home", settings.DOCUMENT_ROOT), ("Code", settings.PREFIX_CODE) ]

        if self.request.getRequestPath() == settings.PREFIX_CODE:
            #
            # Just show the home page of the code browser (list of all installed code)
            #
            data = dict([ (name, { "uri" : Url(class_name().getCodeUri()), "desc" : class_name().getDesc() } ) \
                                for (name, class_name) in _CODE_MAP.items() \
                                    if name[0] not in EXCLUDE_PREFIXES ])
        else:
            # Path elements (the known code prefix is stripped off)
            path_elems = self.request.getRequestPath()[len(settings.PREFIX_CODE):].split("/")[1:]
            component_name  = path_elems[0]   # This should be the name of the code element
            
            # Instantiate the component
            component_class = getComponentClass(self.request.getRequestPath())
            if not component_class:
                return Result.notFound("Unknown component")
            component          = component_class()
            component_home_uri = component.getCodeUri()
            self.breadcrumbs.append((component_name, component_home_uri))

            if len(path_elems) == 1:
                #
                # No sub-detail specified: We want meta info about a code segment (component)
                #
                data = component.getMetaData()
                data = languageStructToPython(component, data)
                self.context_header.append(("[ Create resource ]", settings.PREFIX_RESOURCE+"/_createResourceForm/form/"+component_name, "target=blank"))
            else:
                #
                # Some sub-detail of the requested component was requested
                #
                sub_name = path_elems[1]
                if sub_name == "doc":
                    data       = component.getDocs()
                    self.breadcrumbs.append(("Doc", component_home_uri + "/doc"))
                else:
                    return Result.notFound("Unknown code detail")
                
        return Result.ok(data)
    
    
    def __process_post(self):
        """
        Process a POST request.
        
        The only allowed POST requests to code are requests
        to the base URI of a component. This creates a new resource.
        
        @return:  HTTP return structure.
        @rtype:   Result

        """
        #
        # Start by processing and sanity-checking the request.
        #
        component_class = getComponentClass(self.request.getRequestPath())
        if not component_class:
            return Result.notFound("Unknown component")
        #component = component_class()
        body = self.request.getRequestBody()
        try:
            param_dict = json.loads(body)
        except Exception, e:
            raise GluException("Malformed request body: " + str(e))
        ret_msg = makeResource(component_class, param_dict)
        return Result.created(ret_msg['uri'], ret_msg)
    
    def process(self):
        """
        Process the request.
        
        @return:  HTTP return structure.
        @rtype:   Result
        
        """
        method = self.request.getRequestMethod()
        if method == HTTP.GET_METHOD:
            return self.__process_get()
        elif method == HTTP.POST_METHOD:
            return self.__process_post()
