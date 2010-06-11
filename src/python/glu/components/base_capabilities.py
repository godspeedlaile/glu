"""
Defines a base class for all components.

"""
# Python imports
import urllib, urllib2

import glu.settings as settings

from glu.storageabstraction.file_storage import FileStorage

from org.mulesource.glu.component        import BaseComponentCapabilities
from org.mulesource.glu.component.api    import HttpResult, HTTP

class BaseCapabilities(BaseComponentCapabilities):
    """
    This implements some of the base capabilities, which the framework
    makes available to components of any language. Implemented in Python,
    but by inheriting from a Java interface, it is just as usable from
    within Java.
    
    """
    def __init__(self, component):
        self.__accountname   = None
        self.__password      = None
        self.__my_component  = component

    def getFileStorage(self, namespace=""):
        """
        Return a FileStorage object, which can be used to store data.

        Storage spaces for each resource are separated by resource name,
        this means that two resources cannot share their stored objects,
        even if they are of the same type.

        @param namespace:   A namespace that is used by this resource.
                            Per invocation a resource may chose to create
                            yet another resource namespace under (or within)
                            its inherent namespace.
        @type namespace:    string

        @return:            FileStorage object.

        """
        my_resource_name = self.__my_component.getMyResourceName()
        if my_resource_name:
            if namespace:
                unique_namespace = "%s__%s" % (self.__my_component.getMyResourceName(), namespace)
            else:
                unique_namespace = self.__my_component.getMyResourceName()
            storage = FileStorage(storage_location=settings.STORAGEDB_LOCATION, unique_prefix=unique_namespace)
            return storage
        else:
            # Cannot get storage object when I am not running as a resource
            return None
    
    def __get_http_opener(self, url):
        """
        Return an HTTP handler class, with credentials enabled if specified.
        
        @param url:    URL that needs to be fetched.
        @type url:     string
        
        @return:       HTTP opener (from urllib2)
        
        """
        if self.__accountname  and  self.__password:
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, url, self.__accountname, self.__password)
            authhandler = urllib2.HTTPBasicAuthHandler(passman)
            opener = urllib2.build_opener(authhandler)
        else:
            opener = urllib2.build_opener()
        return opener
        
    def httpSetCredentials(self, accountname, password):
        """
        The component author can set credentials for sites that require authentication.
        
        @param accountname:    Name of account
        @type accountname:     string
        
        @param password:       Password for account.
        @type password:        string
        
        """
        self.__accountname = accountname
        self.__password    = password
    
    def __http_access(self, url, data=None, headers=None):
        """
        Access an HTTP resource with GET or POST.
        
        @param url:        The URL to access.
        @type url:         string
        
        @param data:       If present specifies the data for a POST request.
        @type data:        Data to be sent or None.
        
        @param headers:    A dictionary of additional HTTP request headers.
        @type headers:     dict
        
        @return:           Code and response data tuple.
        @rtype:            tuple
        
        """
        opener = self.__get_http_opener(url)
        # Add any custom headers we might have (list of tuples)
        if headers:
            if type(headers) is not type(dict):
                # If this was called from Java then the headers are
                # defined in a HashMap. We need to translate that to
                # a Python dictionary.
                header_dict = dict()
                header_dict.update(headers)
                headers = header_dict

            opener.addheaders.extend(headers.items())

        resp = opener.open(url, data)
        code = HTTP.OK
        data = resp.read()
        return code, data
        
    def httpGet(self, url, headers=None):
        """
        Accesses the specified URL.
        
        If credentials have been specified, they will be used in case
        of HTTP basic authentication.
        
        @param url:        The URL to be accessed.
        @type url:         string
        
        @param headers:    A dictionary of additional HTTP request headers.
        @type headers:     dict
        
        @return:           HttpResult object.
        @rtype:            HttpResult
        
        """
        res                  =  HttpResult()
        res.status, res.data = self.__http_access(url, headers=headers)
        return res


    def httpPost(self, url, data, headers=None):
        """
        Send the specified data to the specified URL.
        
        If credentials have been specified, they will be used in case
        of HTTP basic authentication.
        
        @param url:        The URL to be accessed.
        @type url:         string
        
        @param data:       The data to be sent to the URL.
        @type data:        string
        
        @param headers:    A dictionary of additional HTTP request headers.
        @type headers:     dict
        
        @return:           HttpResult object.
        @rtype:            HttpResult
        
        """
        res                  =  HttpResult()
        res.status, res.data = self.__http_access(url, data, headers)
        return res
