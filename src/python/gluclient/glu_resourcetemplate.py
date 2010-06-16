"""
Definition of the L{GluResourceTemplate} class.

"""

from gluclient.glu_client_exception import GluClientException
from gluclient.glu_parameter        import GluParameter
from gluclient.glu_service          import GluService

class GluResourceTemplate(object):
    """
    Represents a template that can be used by a client to create a new
    resource.

    The resource template assists the client in setting the required
    resource creation time parameters and provides the method for
    the creation of the new resource.

    """
    # Keys for the directory we post to the server to create a new resource
    __PARAMS_KEY                    = "params"
    __RCP_KEY                       = "resource_creation_params"
    __RCP_DESC_KEY                  = "desc"
    __RCP_PUBLIC_KEY                = "public"
    __RCP_SUGGESTED_NAME_KEY        = "suggested_name"

    def __init__(self, comp):
        """
        Create a new resource template in memory.

        @param comp:      The L{GluComponent} which created this template.
        @type comp:       L{GluComponent}

        """
        self.__component                      = comp
        self.__param_values                   = dict()
        self.__resource_creation_param_values = dict()

    def get_all_parameters(self):
        """
        Return all parameters defined for this template's component.

        @return:    Dictionary of all parameter descriptions.
        @rtype:     dict of L{GluParameter}

        """
        return self.__component.get_all_parameters()

    def get_parameter(self, name):
        """
        Return one parameters of this template's component.

        @param name:    Name of the parameter.
        @type name:     string

        @return:        A parameter description.
        @rtype:         L{GluParameter}

        """
        return self.__component.get_parameter(name)

    def get_resource_description(self):
        """
        Return parameter definition for this template's resource description parameter.

        @return:    The resource description parameter definition.
        @rtype:     L{GluParameter}

        """
        return self.__component.get_resource_description()

    def get_resource_public_flag(self):
        """
        Return parameter definition for this template's resource public flag parameter.

        @return:    The resource public flag parameter definition.
        @rtype:     L{GluParameter}

        """
        return self.__component.get_resource_public_flag()

    def get_resource_suggested_name(self):
        """
        Return parameter definition for this template's resource suggested name parameter.

        @return:    The resource suggested name parameter definition.
        @rtype:     L{GluParameter}

        """
        return self.__component.get_resource_suggested_name()

    def set(self, name, value):
        """
        Set a parameter value for a given parameter.

        Performs proper sanity checking on the type and value.

        @param name:        Name of the parameter.
        @type name:         string

        @param value:       Value of the parameter.
        @type value:        object

        @return:            Reference to ourselves, so that set() calls can be chained
        @rtype:             L{GluResourceTemplate}

        """
        pdef = self.get_parameter(name)
        pdef.sanity_check(value)
        self.__param_values[name] = value

        return self

    def set_params(self, params):
        """
        Set values of multiple parameters from a dictionary.

        Performs proper sanity checking on the type and value
        of each parameter.

        @param params:    Dictionart of name/values for the parameters
                          of this resource template.
        @type params:     dict

        @return:          Reference to ourselves, so that set() calls can be chained
        @rtype:           L{GluResourceTemplate}

        """
        for name, value in params.items():
            self.set(name, value)
        return self

    def set_description(self, desc):
        """
        Sets the 'description' resource creation time parameter.

        @param desc:    Description for the new resource.
        @type desc:     string

        @return:        Reference to ourselves, so that set() calls can be chained
        @rtype:         L{GluResourceTemplate}

        """
        if type(desc) not in [ str, unicode ]:
            raise GluClientException("Description needs to be of type string or unicode, not '%s'." % type(desc))
        self.__resource_creation_param_values[self.__RCP_DESC_KEY] = desc

        return self

    def set_public_flag(self, flag):
        """
        Sets the 'public' resource creation time parameter.

        @param flag:    Public flag for the new resource.
        @type flag:     bool

        @return:        Reference to ourselves, so that set() calls can be chained
        @rtype:         L{GluResourceTemplate}

        """
        if type(flag) is not bool:
            raise GluClientException("Public flag needs to be of type bool, not '%s'." % type(flag))
        self.__resource_creation_param_values[self.__RCP_PUBLIC_KEY] = flag

        return self

    def set_suggested_name(self, name):
        """
        Sets the 'suggested name' resource creation time parameter.

        @param name:    Suggested name for the new resource.
        @type name:     string

        @return:        Reference to ourselves, so that set() calls can be chained
        @rtype:         L{GluResourceTemplate}

        """
        if type(name) not in [ str, unicode ]:
            raise GluClientException("Suggested name needs to be of type string or unicode, not '%s'." % type(name))
        self.__resource_creation_param_values[self.__RCP_SUGGESTED_NAME_KEY] = name

        return self

    def create_resource(self):
        """
        Posts a new resource description to the server.

        Returns an initialized L{GluResource} object, ready to use.

        """
        # Check if all mandatory parameters have been set
        for name, pdef in self.get_all_parameters().items():
            if pdef.is_required():
                if name not in self.__param_values:
                    raise GluClientException("Required parameter '%s' is missing." % name)

        d = dict()
        d[self.__PARAMS_KEY] = self.__param_values
        d[self.__RCP_KEY]    = self.__resource_creation_param_values

        res = self.__component._create_resource(d)
        if res['status'] != "created":
            raise GluClientException("Resource could not be created.")

        name = res['name']

        return self.__component.get_server().get_resource(name)


    #
    # For convenience, we offer write access to those settable
    # elements via properties.
    #
    suggested_name = property(None, set_suggested_name)
    public         = property(None, set_public_flag)
    description    = property(None, set_description)
    params         = property(None, set_params)

