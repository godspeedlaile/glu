"""
The request dispatcher class, which directs requests
to the appropriate browsers.

"""
# Glu imports
import glu.settings as settings

from org.mulesource.glu.exception             import *
from org.mulesource.glu.component.api         import HTTP, Result

from glu.core.basebrowser       import BaseBrowser
from glu.core.staticbrowser     import StaticBrowser
from glu.core.metabrowser       import MetaBrowser
from glu.core.codebrowser       import CodeBrowser 
from glu.core.resourcebrowser   import ResourceBrowser 

BROWSER_MAP   = {
                    settings.PREFIX_META     : MetaBrowser,
                    settings.PREFIX_RESOURCE : ResourceBrowser,
                    settings.PREFIX_CODE     : CodeBrowser,
                    settings.PREFIX_STATIC   : StaticBrowser,
                }
            
class RequestDispatcher(object):
    """
    Takes incoming HTTP requests and sends them off to the
    appropriate modules.
    
    """
    def handle(self, request):
        """
        Handle a request by dispatching it off to the correct handler.
        
        The handler is a 'browser' class, which can be looked up via the
        BROWSER_MAP that is defined in the settings file.
        
        This also catches any GluExceptions thrown by lower level code and
        translates them into log messages.
        
        @param request:   A properly wrapped request.
        @type request:    GluHttpRequest
        
        @return:          Response structure and headers
        @rtype:           Tuple of (Result, dict)
        
        """
        #print "---- ", request.getRequestHeaders()
        content_type = None
        try:
            if request.getRequestPath() == "/":
                browser_class = BROWSER_MAP['/meta']
            else:
                method        = request.getRequestMethod().upper()
                prefix        = "/"+request.getRequestPath().split("/")[1]
                browser_class = BROWSER_MAP.get(prefix)
            
            if browser_class:
                browser_instance = browser_class(request)
                result           = browser_instance.process()
                if result.getStatus() >= 200  and  result.getStatus() < 300:
                    headers = result.getHeaders()
                    # Check if the Content-type return header was set by
                    # the component. If so, we assume that the component
                    # has returned data in the appropriate format already
                    # and we will not perform any encoding.
                    # For example, if an image file is returned then the
                    # component may have set the content type to "image/jpg".
                    if headers:
                        content_type = result.getHeaders().get("Content-type")
                    else:
                        content_type = None
                    if content_type is None:
                        # If all was OK with the request then we will
                        # render the output in the format that was
                        # requested by the client. But only if we don't
                        # have a content-type set on this request already.
                        content_type, data = browser_instance.renderOutput(result.getEntity())
                        result.setEntity(data)
            else:
                result = Result.notFound("Not found" )
        except GluMethodNotAllowedException, e:
            result = Result(e.code, e.msg)
        except GluMandatoryParameterMissingException, e:
            result = Result(e.code, e.msg)
        except GluFileNotFoundException, e:
            result = Result(e.code, e.msg)
        except GluException, e:
            result = Result.badRequest("Bad request: " + e.msg)

        if content_type:
            result.addHeader("Content-type", content_type);
        
        return result

