
This is Glu.

For full documentation please visit:

    http://glu.mulesoft.com


For Windows installation instructions, please see: 

    http://glu.mulesoft.org/installing-and-running-windows


For the quick start guide, please see:

    http://glu.mulesoft.org/quick-start-guide



Files
=====
You can see the following files and directories:

install.sh      The installation script for Linux/Unix. It performs necessary
                sanity checks on the environment, installs Jython if necessary
                and constructs various helper scripts.

gluctl          The main control script for Glu. Built during the install.
                Used to start/stop the server, create and install new components,
                and so on.

conf/           Contains the doc string for the server as well as the version
                number.

bin/            Contains most of the helper scripts, which are created during
                the install.

lib/            Location for JAR files.

languages/      Contains language specific component templats and tools.

src/            Contains the source code

src/python      Contains the Python code (this includes some test utilities).
                The glu/ directory there contains most of the code. starter.py
                and glujson.py are the exception.

src/java        Contains the java code.

src/python/starter.py  The start script for the Glu server. No need to call it
                directly. The gluctl script performs all the necessary steps
                for you.

static_files/   The directory from where the Glu erver can serve static files.

resourceDB/     This is where the Glu server stores resource definitions.

storageDB/      This is where the file-storage facility for components stores
                its files.

tools/          Holds a few third party sources we are bundling to reduce dependencies
                during install.


