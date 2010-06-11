"""
Base class from which all storage abstractions derive.

"""
import glujson as json

# Glu imports
from glu.storageabstraction.file_storage import FileStorage
from org.mulesource.glu.exception        import *

class ResourceStorage(FileStorage):
    """
    Implementation of resource storage methods.

    """

    def loadResourceFromStorage(self, resource_name):
        """
        Load the specified resource from storage.

        @param resource_name:    Name of the selected resource.
        @type resource_name:     string

        @return                  A Python dictionary representation or None
                                 if not found.
        @rtype                   dict

        """
        try:
            buf = self.loadFile(resource_name)
        except GluFileNotFoundException, e:
            return None
        obj = json.loads(buf)
        return obj

    def deleteResourceFromStorage(self, resource_name):
        """
        Delete the specified resource from storage.

        @param resource_name:    Name of the selected resource.
        @type resource_name:     string

        """
        self.deleteFile(resource_name)

    def listResourcesInStorage(self):
        """
        Return list of resources which we currently have in storage.

        @return:                 List of resource names.
        @rtype:                  list

        """
        try:
            dir_list = self.listFiles()
            return dir_list
        except Exception, e:
            raise GluException("Problems getting resource list from storage: " + str(e))

    def writeResourceToStorage(self, resource_name, resource_def):
        """
        Store a resource definition.
        
        No return value, but raises GluException if there is an issue.
        
        @param resource_name: The storage name for this resource
        @type  resource_name: string
        
        @param resource_def: The dictionary containing the resource definition.
        @type  resource_def: dict
        
        @raise GluException: If the resource cannot be stored.
            
        """
        try:
            buf = json.dumps(resource_def, indent=4)
            self.storeFile(resource_name, buf)
        except Exception, e:
            raise GluException("Problems storing new resource: " + str(e))

