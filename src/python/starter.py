



"""
Simple starter for stand-alone Glu server.

"""
import os
import sys
import time
import getopt

# Glu imports
import glu.settings as settings
import glu.logger   as logger

from glu.core                import RequestDispatcher
from glu.platform_specifics  import *

from org.mulesource.glu      import Settings
from org.mulesource.glu.util import Url

from org.mulesource.glu.component.api import *

def print_help():
    print \
"""
Glu server (c) 2010 MuleSoft

Usage:  jython starter.py  [options]

Options:
        -h, --help
                Print this help screen.

        -P, --port <num>
                Port on which the server listens for requests.

        -p, --pidfile <filename>
                If specified, the PID of the server is stored in <filename>.

        -l, --logfile <filename>
                If specified, the filename for the logfile. If not specified,
                output will go to the console.
"""


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:P:p:", ["help", "logfile=", "port=", "pidfile="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        print_help()
        sys.exit(1)

    port = settings.LISTEN_PORT
    for o, a in opts:
        if o in ("-p", "--pidfile"):
            # Writing our process ID
            pid = os.getpid()
            f = open(a, "w")
            f.write(str(pid))
            f.close()
        elif o in ("-h", "--help"):
            print_help()
            sys.exit(0)
        elif o in ("-P", "--port"):
            port = int(a)
        elif o in ("-l", "--logfile"):
            logger.set_logfile(a)
            
    my_server = HttpServer(port, RequestDispatcher())

