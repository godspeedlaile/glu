
"""
Definition of the GluService class.

"""
import urllib

from gluclient.glu_client_exception import GluClientException
from gluclient.glu_parameter        import GluParameter

class HttpResult(object):
    status = None
    data   = None

class GluService(object):
    """
    Represents information about a service of a Glu component or resource.

    This representation can be used by clients to find out about
    service capabilities.

    """
    # The keys to the component's meta data dictionary.
    __DESC_KEY                      = "desc"
    __URI_KEY                       = "uri"
    __PARAMS_KEY                    = "params"
    __POSITIONAL_PARAMS_KEY         = "positional_params"

    __name                          = None   # Name of this component
    __description                   = None   # Description of this component
    __uri                           = None   # URI of this component
    __parameters                    = None   # Dictionary of parameter definitions
    __positional_params             = None   # List of positional parameters

    def __str__(self):
        """
        Return a string representation of this service.

        """
        buf = \
"""GluService: %s
    Description:           %s
    Positional parameters: %s
    Parameters:""" % (self.__name, self.__description, self.__positional_params)
        if self.__parameters:
            for pname, pdef in self.__parameters.items():
                buf += "\n----------------\n" + str(pdef)
        return buf

    def __init__(self, name, sdesc):
        """
        Create a new service representation in memomory.
        
        @param name:        Name of this service.
        @type name:         string

        @param sdesc:       Dictionary describing the service. This
                            is the dictionary returned by the server when a
                            component or resource is accessed.
        @type sdesc:        dict

        """
        try:
            self.__name              = name
            self.__description       = sdesc[self.__DESC_KEY]
            self.__uri               = sdesc[self.__URI_KEY]
            self.__positional_params = sdesc.get(self.__POSITIONAL_PARAMS_KEY)
            pdict                    = sdesc.get(self.__PARAMS_KEY)

            # Parse the parameter dictionary and attempt to translate
            # this to a dictionary of proper GluParameter objects.
            if pdict:
                self.__parameters = dict()
                for pname, pdef in pdict.items():
                    self.__parameters[pname] = GluParameter(pname, pdef)

        except KeyError, e:
            raise GluClientException("Server error: Expected key '%s' missing in definition of service '%s'." % (str(e), self.__name))

    def get_name(self):
        """
        Return the name of the component.

        @return:    Name of component.
        @rtype:     string

        """
        return self.__name

    def get_description(self):
        """
        Return the description of the component.

        @return     Description of the component.
        @rtype:     string

        """
        return self.__description

    def get_uri(self):
        """
        Return the URI of the component.

        @return     URI of the component.
        @rtype:     string

        """
        return self.__uri

    def get_all_parameters(self):
        """
        Return all parameters defined for this component.

        @return:    Dictionary of all parameters.
        @rtype:     dict of GluParam

        """
        return self.__parameters

    def get_parameter(self, name):
        """
        Return one parameters of this component.

        @param name:    Name of the parameter.
        @type name:     string

        @return:        Dictionary of all parameters.
        @rtype:         dict of GluParam

        """
        try:
            return self.__parameters[name]
        except KeyError:
            raise GluClientException("Parameter '%s' not defined." % name)

    def get_positional_param_names(self):
        """
        Return list of positional parameters."

        @return:        List of positional parameters.
        @rtype:         list

        """
        return self.__positional_params


class GluAccessibleService(GluService):
    """
    Represents information about a service of a Glu component or resource,
    ready to be accessed.

    This representation can be used by clients to find out about
    service capabilities and also to access the service methdods of
    the resource.

    """
    __param_vals = None         # Dictionary with name/value pairs for the service method
    __input_buf  = None         # Information that should be sent to the service method in
                                # the request body
    __resource   = None         # Reference to this service's resource

    def __init__(self, resource, name, sdesc):
        """
        @param name:        Name of this service.
        @type name:         string

        @param sdesc:       Dictionary describing the service. This
                            is the dictionary returned by the server when a
                            component or resource is accessed.
        @type sdesc:        dict

        """
        super(GluAccessibleService, self).__init__(name, sdesc)
        self.__param_vals = dict()
        self.__resource   = resource

    def set(self, name, value):
        """
        Specify a parameter value for the service method.

        The string representation of the 'value' object is
        stored. This parameter value will be passed on the
        URL command line.

        @param name:        Name of the parameter.
        @type name:         string

        @param value:       The value for the parameter.
        @type value:        Any type for which we can use str()

        @return:            Reference to ourselves, so that set() calls can be chained
        @rtype:             GluAccessibleService

        """
        pdef = self.get_parameter(name)
        pdef.sanity_check(value)
        self.__param_vals[name] = str(value)
        return self

    def set_params(self, param_dict):
        """
        Set the parameters for the service method specified in the dictionary.

        The string representations of each parameter value are stored.

        @param param_dict:  Dictionary with name/value pairs.
        @type param_dict:   dict

        @return:            Reference to ourselves, so that set() calls can be chained
        @rtype:             GluAccessibleService

        """
        for name, value in param_dict.items():
            self.set(name, value)
        return self

    def set_input(self, buf):
        """
        Specify an input buffer that's to be sent in the
        request to the service method.

        @param buf:     Content for the message body.
        @type buf:      string

        @return:        Reference to ourselves, so that set() calls can be chained
        @rtype:         GluAccessibleService

        """
        self.__input_buf = buf

    def access(self, method=None):
        """
        Sends the service request to the server.

        @param method:  The HTTP request method. If an input was set then this
                        defaults to POST. If the caller requests anything but
                        PUT or POST with a set input then an exception is raised.
                        If no input was specified then method defaults to GET.
        @type mthod:    string

        @return:        An HttpResult structure with information about the server
                        response.
        @rtype:         HttpResult

        """
        # Assemble the request URI
        qs = urllib.urlencode(self.__param_vals)
        uri = self.__resource.get_uri() + "/" + self.get_name() + (("?%s" % qs) if qs else "")

        if method is None:
            # Caller didn't specify method, so we set a default one.
            if self.__input_buf:
                method = "POST"
            else:
                method = "GET"
        else:
            # A method was specified by the caller. Do some sanity checking.
            # Specifically: If an input was specified then the method must be
            # either POST or PUT
            method = method.upper()
            if self.__input_buf:
                if method not in ["POST", "PUT"]:
                    raise GluClientExcetion("Request method must be POST or PUT, because a message body (input) was set.")
            else:
                if method not in ["GET", "HEAD", "OPTIONS", "DELETE"]:
                    if method in ["POST", "PUT"]:
                        raise GluClientExcetion("Cannot specify POST or PUT request method without setting message body (input).")
                    else:
                        raise GluClientException("Unknown request method '%s'." % method)

        server       = self.__resource.get_server()
        status, data = server._json_send(uri, data=self.__input_buf, method=method)
        return status, data

