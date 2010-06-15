"""
A sample template for Glu components, written in Python.

"""
from glu.components.api import *

class WordCount(BaseComponent):
    NAME             = "WordCount"
    DESCRIPTION      = "POST text and get back a word count."
    DOCUMENTATION    = "A word counter for arbitrary text."

    PARAM_DEFINITION = {}
    
    # A dictionary with information about each exposed service method (sub-resource).
    SERVICES         = {
                           "count" : {
                               "desc" : "Counts words in a posted text",
                           }
                       }
        

    def count(self, method, input):
        """
        The foobar service method.
        
        @param method:     The HTTP request method.
        @type method:      string
        
        @param input:      Any data that came in the body of the request.
        @type input:       string

        @return:           The output data of this service.
        @rtype:            Result

        """
        if input:
            elems = input.strip().split()
            num_words = len(elems)
        else:
            num_words = 0

        return Result.ok(num_words)

