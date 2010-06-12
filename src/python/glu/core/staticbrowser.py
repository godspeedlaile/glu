"""
Serves static files.

"""
import glu.settings as settings

from glu.core.basebrowser import BaseBrowser

from org.mulesource.glu.component.api import HTTP, Result

        
class StaticBrowser(BaseBrowser):
    """
    Handles requests for meta data of the server.
    
    Meta data here is defined as non-code and non-resource data.
    For example, the name of the server, version number, links to
    the other, more interesting sections, etc.
    
    Just contains a bunch of static links.
    
    """
    def __init__(self, request):
        """
        Create the new meta browser for a request.
        
        @param request:  The client's HTTP request.
        @type request:   GluHttpRequest
        
        """
        # Initialize the browser with the render-args we need for meta data browsing
        super(StaticBrowser, self).__init__(request,
                                            renderer_args = dict(raw=True))

    def process(self):
        """
        Process the request.
        
        Produce the data that needs to be displayed for any request
        handled by this browser. Currently, there is only one request
        handled by the meta browser.
        
        @return:  Http return code and data as a tuple.
        @rtype:   tuple
        
        """
        path = self.request.getRequestPath()[len(settings.PREFIX_STATIC)+1:]
        if ".." in path:
            # Won't allow that
            return HTTP.BAD_REQUEST, "Invalid path specifier"
        if path.endswith("/"):
            path = path[:-1]
            
        try:
            f = open(settings.get_root_dir()+settings.STATIC_LOCATION + path, "r")
            data = f.read()
            f.close()
            res = Result.ok(data)
            # Examine the extension of the filename to see if we can set the content
            # type based on any of them. If we set the content type here then the
            # request dispatcher will not attempt to call a render method on the
            # data we return.
            i = path.rfind(".")
            if i > -1:
                # Found an extension in the filename
                ext = path[i+1:].lower()
                if ext in [ "jpg", "png", "gif", "jpeg" ]:
                    res.addHeader("Content-type", "image/%s" % ext)
            return res
        except Exception, e:
            return Result.notFound("Not found")
            
