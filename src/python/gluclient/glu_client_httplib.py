
import urlparse
import string
import httplib
import base64
import urllib
import re
import socket



class HttpResponse:

    def __init__(self, get_response_now, connection, my_instance_counter, dbg_str=None):
        """
        Takes the HTTPConnection object as initializer.
        The dbg_str is printed when the connection is closed,
        if it is something other than None. The get_response_now
        flag indicates whether we should try to receive the response
        from the server right here, or leave this to the user for
        later. Finally, the my_instance_counter is mostly used
        for internal tracking and debugging.

        In general: A user should not try to create this kind
        of object on its own. The urlopn() and sendreq() functions
        of this module are the only ones who should do so.
        """
        try:
            self.__connection = connection
            self.__counter    = my_instance_counter
            if get_response_now:
                self.__response = connection.getresponse()
            else:
                self.__response = None
            self.__headers    = None
            self.__dbg_str    = dbg_str
        except Exception, e:
            print "SnapHttpLib.HttpResponse.__init__(): Exception: " + str(e)
            raise e
        
    def sock():
        """The socket inside HttpConnection of HttpResponse (depending on object which is active)"""
        doc = "Socket wrapped by HttpResponse or HttpConnection."
        def fget(self):
            if self.__response:
                return self.__response.fp
            else:
                return self.__connection.sock
        return locals()
    sock = property(**sock())

    def isResponseReceived(self):
        if self.__response is not None:
            return True
        else:
            return False

    def getResponse(self):
        if self.__response is None:
            self.__response = self.__connection.getresponse()
        else:
            raise Exception("Network error: Response was already received...")
        
    def write(self, data):
        '''
            Writes data and response has not yet been received.
        '''
        if self.__response is not None:
            raise Exception("Network error: Response has already been received...")
        try:
            return self.__connection.send(data)
        except Exception, e:
            raise e

    def getStatus(self):
        '''
            Returns the numeric value of the HTTP response code,
            such as 200, 404, etc.
        '''
        if self.__response is None:
            raise Exception("Network error: Response has not been received yet...")
        return self.__response.status

    def getReason(self):
        '''
            Returns the reason for a failure.
        '''
        if self.__response is None:
            raise Exception("Network error: Response has not been received yet...")
        return self.__response.reason

    def getHeaders(self):
        '''
            Returns the HTTP response headers as a dictionary.
        '''
        if self.__response is None:
            raise Exception("Network error: Response has not been received yet...")
        try:
            if self.__headers is None:
                # The HTTPresponse object can give us a list of tuples of the
                # server's response headers. Let's make a dictionary out of it,
                # for our convenience.
                h = self.__response.getheaders()
                self.__headers = {}
                [ self.__headers.__setitem__(hdr, val) for (hdr, val) in h ]
        except Exception, e:
            print "SnapHttpLib.HttpResponse.getHeaders(): Exception: " + str(e)
            raise e
        return self.__headers

    def read(self, num=None):
        '''
            Reads the specified number of bytes from the server, or (if
            no number of bytes is specified) as much as possible.
        '''
        if self.__response is None:
            raise Exception("Network error: Response has not been received yet...")
        try:
            return self.__response.read(num)
        except Exception, e:
            print "SnapHttpLib.HttpResponse.read(" + str(num) + "): Exception: " + str(e)
            raise e
        
    def close(self):
        '''
            Closes the connection.
        '''
        try:
            if self.__dbg_str is not None:
                print "--- c_" + str(self.__counter) + ". SnapHttpLib.HttpResponse.close (" + str(self.__dbg_str) + ")"
            self.__connection.close()
        except Exception, e:
            print "SnapHttpLib.HttpResponse.close(): Exception: " + str(e)
            raise e
        
        if self.__response is not None:
            try:
                self.__response.close()
            except Exception, e:
                print "SnapHttpLib.HttpResponse.close(): Response Exception: " + str(e)
                raise e


def setUsernamePassword(username, password):
    _HttpAuthenticationHolder._setUsernamePassword(username, password)

def sendreq(method, url, data=None, headers=None, credential=None, timeout=None):
    '''
        Opens a URL. A great deal of flexibility is offered.

            method:     "GET", "POST", "DELETE", PUT"
            url:        The actual, full, URL that we want to reach.
            data:       Any data in message body.
            headers:    Dictionary of HTTP request headers.
            credential: A 2-tuple containing (username, password)
            timeout:    A nonnegative float expressing seconds, or None.

        Returns a HttpResponse object. That object then is used to
        look at the server response and also read data from the
        connection.

        Note that this function here returns without actually having
        requested (read) the initial response from the server. That
        needs to be done by the user of this function by calling the
        getResponse() method on the response object. You can use
        isResponsReceived() on the response to see if that has taken
        place already.
    '''

    (scheme, host, path, params, query, fragment) = urlparse.urlparse(url)
    rempath = urlparse.urlunparse((None, None, path, params, query, None))

    if headers is None:
        headers = {}

    if scheme == 'https':
        conn = httplib.HTTPSConnection(host)
    else:
        conn = httplib.HTTPConnection(host)

    conn.request(method.upper(), rempath, data, headers)

    # return HttpResponse(False, conn, counter, str((method, url, headers)))
    return HttpResponse(False, conn, counter, None)


def urlopen(method, url, data=None, headers=None, credential=None, timeout=None):
    '''
        Opens a URL. Similar to sendreq(), except that this one tries to
        get the response from the server right away.

            method:     "GET", "POST", "DELETE", PUT"
            url:        The actual, full, URL that we want to reach.
            data:       Any data in message body.
            headers:    Dictionary of HTTP request headers.
            credential: A 2-tuple containing (username, password)
            timeout:    A nonnegative float expressing seconds, or None.

        Returns a HttpResponse object.
    '''
    r = sendreq(method, url, data, headers, credential, timeout)
    r.getResponse()
    return r

