
"""
Definition of the GluClient API.

This makes available the following classes:

    GluClientException
    GluComponent
    GluParameter
    GluServer

Usage example:

    #
    # Connect to a server
    #
    srv = GluServer("http://localhost:8001")

"""
from gluclient.glu_client_exception import *
from gluclient.glu_component        import GluComponent
from gluclient.glu_parameter        import GluParameter
from gluclient.glu_server           import GluServer
from gluclient.glu_service          import GluService, GluAccessibleService, HttpResult
from gluclient.glu_resource         import GluResource
from gluclient.glu_resourcetemplate import GluResourceTemplate


