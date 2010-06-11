"""
Base class from which all storage abstractions derive.

"""

# Python imports
import os

# Glu imports
import glu.settings as settings
from org.mulesource.glu.exception     import *
from org.mulesource.glu.component.api import FileStore

class FileStorage(FileStore):
    """
    Abstract implementation of the base storage methods.

    """
    def __init__(self, storage_location, unique_prefix=""):
        """
        The unique prefix is used to create a namespace in a flat bucket.

        """
        self.storage_location = storage_location
        self.unique_prefix    = unique_prefix

    def _get_storage_location(self):
        return settings.get_root_dir()+self.storage_location

    def __make_filename(self, file_name):
        if self.unique_prefix:
            name = "%s/%s__%s" % (self._get_storage_location(), self.unique_prefix, file_name)
        else:
            name = "%s/%s" % (self._get_storage_location(), file_name)
        return name

    def __remove_filename_prefix(self, file_name):
        if self.unique_prefix:
            if file_name.startswith(self.unique_prefix):
                file_name = file_name[len(self.unique_prefix) + 2:]
        return file_name

    def loadFile(self, file_name):
        """
        Load the specified file from storage.

        @param file_name:    Name of the selected file.
        @type file_name:     string

        @return              Buffer containing the file contents.
        @rtype               string

        """
        try:
            f   = open(self.__make_filename(file_name), "r")
            buf = f.read()
            f.close()
        except Exception, e:
            raise GluFileNotFoundException("File '%s' could not be found'" % (file_name))
        return buf

    def storeFile(self, file_name, data):
        """
        Store the specified file in storage.

        @param file_name:    Name of the file.
        @type file_name:     string

        @param data:         Buffer containing the file contents.
        @type data:          string

        """
        f = open(self.__make_filename(file_name), "w")
        f.write(data)
        f.close()

    def deleteFile(self, file_name):
        """
        Delete the specified file from storage.

        @param file_name:    Name of the selected file.
        @type file_name:     string

        """
        try:
            os.remove(self.__make_filename(file_name))
        except OSError, e:
            if e.errno == 2:
                raise GluFileNotFoundException(file_name)
            elif e.errno == 13:
                raise GluPermissionDeniedException(file_name)
            else:
                raise GluException("Cannot delete file '%s (%s)'" % (file_name, str(e)))
        except Exception, e:
            raise GluException("Cannot delete file '%s' (%s)" % (file_name, str(e)))

    def listFiles(self):
        """
        Return list of all files in the storage.

        @return:                 List of file names.
        @rtype:                  list

        """
        try:
            dir_list = os.listdir(self._get_storage_location())
            # Need to filter all those out, which are not part of our storage space
            if self.unique_prefix:
                our_files = [ name for name in dir_list if name.startswith(self.unique_prefix) ]
            else:
                our_files = dir_list
            no_prefix_dir_list = [ self.__remove_filename_prefix(name) for name in our_files ]
            return no_prefix_dir_list
        except Exception, e:
            raise GluException("Problems getting file list from storage: " + str(e))

