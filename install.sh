#!/bin/bash

# Installer for Glu

JYTHON_DOWNLOAD_LOCATION="http://downloads.sourceforge.net/project/jython/jython/2.5.1/jython_installer-2.5.1.jar"
JYTHON_DOWNLOAD_FILE="jython_installer.jar"
DEFAULT_INSTALL_DIR="`pwd`/jython"
ENVIRON_TMP_FILE="__glustart_tmp"
CTL_SCRIPT_BODY="bin/frags/_ctl_frg"
CTL_SCRIPT="gluctl"
COMPILE_SCRIPT_BODY="bin/frags/_compile_frg"
COMPILE_SCRIPT="glucompile"
COMPILE_SCRIPT_DIR="bin"
PID_FILE="glu.pid"

# ---------------------------------------------
# Helper functions
# ---------------------------------------------

function error_report
{
    echo -e "\nError: "$1"\n"
}

# Test whether an executable can be found.
# Name of executable as 1. param
# Error text as 2. param
# Flag value ('y' or 'n') as 3. param indicates
# whether we exit in case of error ("n" or if not defined), or return 1 ("y").
# The found executable is returned in $EXEC_PATH variable.
EXEC_PATH=""
function exec_test
{
    EXEC_TEST=`builtin type -P $1`
    if [ -z "$EXEC_TEST" ]; then

        error_report "I can't find a '$1' executable.\n""$2"
        if [ -z "$3"  -o  "$3" == "n" ]; then
            exit 1
        else
            return 1
        fi
       
    else

        echo "Ok. Found '$1' executable at: "$EXEC_TEST
        EXEC_PATH=$EXEC_TEST
        return 0
    fi
}

# Tests whether wget or curl are installed and uses
# whichever is available to download the specified URI (1. param).
# The output is stored in the file specified with the 2. param.
function download
{
    WGET_TEST=`builtin type -P wget`
    CURL_TEST=`builtin type -P curl`
    if [ -n "$WGET_TEST" ]; then
        wget $1 -O $2
    elif [ -n "$CURL_TEST" ]; then
        curl -L $1 -o $2
    else
        error_report "Need 'wget' or 'curl' for download."
        exit 1
    fi
}

# Append two file ($1 head and $2 body), set execute flag on
# the result and finally move into a designated location ($3).
function script_combiner {
    cat $1 $2 > __tmp_script_combiner
    if [ $? == 1 ]; then
        error_report "Cannot append '$2' to '$1' in location '__tmp_script_combiner'. Abort..."
        exit 1
    fi

    chmod u+x __tmp_script_combiner
    if [ $? == 1 ]; then
        error_report "Cannot give execute permissions to '__tmp_script_combiner'. Abort..."
        exit 1
    fi

    mv __tmp_script_combiner $3
    if [ $? == 1 ]; then
        error_report "Cannot move '__tmp_script_combiner' to '$3'. Abort..."
        exit 1
    fi
}


# ---------------------------------------------
# Main program
# ---------------------------------------------

echo -e "\n=== Welcome to the Glu installer.\n=== (c) 2010 MuleSoft.
===
=== Please see LICENSE.TXT for the complete license.
===
=== This script performs the necessary dependency checks, assists in the install
=== of necessary software, builds and starts Glu and runs initial tests.
"

# Create the new start script for the Glu server in a temporary
# location so that we don't clobber the current install script
# and leave the user hanging, in case something goes wrong during
# this run.
echo -e "#!/bin/bash\n\n# Auto generated during install...\n\n" > $ENVIRON_TMP_FILE

# Check whether a proper JVM is installed.
exec_test "java" "Please install a JAVA SDK (at least version 1.6) and make it available in the path."
JAVA_EXECUTABLE=$EXEC_PATH
echo 'JAVA_EXECUTABLE='$JAVA_EXECUTABLE >> $ENVIRON_TMP_FILE

exec_test "javac" "Please install a Java SDK (at least version 1.6) and make it available in the path."
JAVAC_EXECUTABLE=$EXEC_PATH
echo 'JAVAC_EXECUTABLE='$JAVAC_EXECUTABLE >> $ENVIRON_TMP_FILE

# Check version of the java compiler and java runtime
case "`javac -version 2>&1`" in 
  *1.6*) ;;
  *) error_report "Installed Java compiler does not seem to be version 1.6."
     exit 1;;
esac 
case "`java -version 2>&1`" in 
  *1.6*) ;;
  *) error_report "Installed Java run time does not seem to be version 1.6."
     exit 1;;
esac 

# Check for Jython install
JYTHON_HOME=
install_needed=0
exec_test "jjython" "Jython 2.5.1 could not be found." "y"
if [ $? == 1 ]; then
    #
    # Jython was not found. Does it exist already on the system?
    #
    while [ 1 ] ; do
        read -p "Do you have Jython installed already? (y/n): " ui
        if [ ! -z $ui ]; then
            if [ $ui == "y" ]; then
                read -p "Please specify the Jython install directory: " install_dir
                JYTHON_HOME="`cd $install_dir; pwd`"
                exec_test "$JYTHON_HOME/jython" "The specified Jython directory does not contain a jython executable."
                break
            elif [ $ui == "n" ]; then
                install_needed=1
                break
            fi
        fi
    done
fi

if [ $install_needed == 1 ]; then
    #
    # Jython was not found. Does the user want us to install Jython manually?
    #
    echo -e "Jython 2.5.1 needs to be installed. Would you like me to install it for you now?
If not then you will have to install it manually."
    read -p "Attempt automatic install of Jython? (Y/n): " ui
    if [ -z $ui ]; then
        ui="y"
    fi
    if [ $ui == "n" ]; then
        error_report "No Jython install is available. Please install Jython manually and then try again.\nBye for now..."
        exit 1
    else
        # Attempting automatic install of Jython
        echo -e "\nStarting automatic install of Jython."
        if [ -f "$JYTHON_DOWNLOAD_FILE" ]; then
            echo "Found copy of $JYTHON_DOWNLOAD_FILE. Skipping download..."
        else
            echo -e "Please wait for download from: "$JYTHON_DOWNLOAD_LOCATION"...\n-------------------------------------------------"
            download $JYTHON_DOWNLOAD_LOCATION $JYTHON_DOWNLOAD_FILE
            echo "-------------------------------------------------"
        fi

        # We have the jython installer file now. Let's find a good install directory
        echo -e "\nPlease specify the install location for Jython."
        retry_flag=1
        while [ $retry_flag == 1 ]; do
            read -p "Enter install directory or press enter to accept default ($DEFAULT_INSTALL_DIR): " install_dir
            if [ -z "$install_dir" ]; then
                install_dir=$DEFAULT_INSTALL_DIR
            fi
            echo "Chosen install dir: " $install_dir
            if [ -f $install_dir ]; then
                read -p "This is not a directory, but an ordinary file. Can I erase the file and create the directory (y/N) ? " choice
                if [ ! -z $choice ]; then
                    if [ $choice == "y" ]; then
                        rm $install_dir
                        retry_flag=0
                    fi
                fi
            elif [ -d $install_dir ]; then
                read -p "The chosen install directory exists already. Can I erase and re-create the directory (y/N) ? " choice
                if [ ! -z $choice ]; then
                    if [ $choice == "y" ]; then
                        rm -rf $install_dir
                        retry_flag=0
                    fi
                fi
            elif [ -e $install_dir ]; then
                echo "Cannot create directory at that location. Please specify an alternative..."
            else
                retry_flag=0
            fi
        done

        # We have the directory, so the install can commence
        java -jar jython_installer.jar -s -t standard -d $install_dir
        if [ $? == 1 ]; then
            error_report "The Jython install failed. Please attempt to correct the problem and try again. By for now..."
            exit 1
        fi

        JYTHON_HOME="`cd $install_dir; pwd`"
        echo "Jython has been installed."
    fi
else
    JYTHON_EXECUTABLE=$EXEC_PATH
    if [ -z "$JYTHON_HOME" ]; then
        echo "Found the 'jython' executable, but don't have "'$JYTHON_HOME variable set.'
        read -p "Please specify the Jython install directory: " install_dir
        JYTHON_HOME="`cd $install_dir; pwd`"
    fi
fi

#
# Sanity checking the Jython home directory
#
JYTHON_EXECUTABLE=$JYTHON_HOME/jython
JYTHON_JAR=$JYTHON_HOME/jython.jar
if [ ! -f $JYTHON_EXECUTABLE ]; then
    error_report "Jython install does not appear to be successful. Cannot find '$JYTHON_EXECUTABLE'."
    exit 1
fi
if [ ! -f $JYTHON_JAR ]; then
    error_report "Jython install does not appear to be successful. Cannot find '$JYTHON_JAR'."
    exit 1
fi
echo "Jython install directory appears to be in good shape."

# Checking the installed version of Jython
case "`$JYTHON_EXECUTABLE -V 2>&1`" in 
  *2.5*) ;;
  *) error_report "Installed jython does not seem to be version 2.5.*"
     exit 1;;
esac 

echo 'JYTHON_HOME='$JYTHON_HOME >> $ENVIRON_TMP_FILE
echo 'JYTHON_EXECUTABLE='$JYTHON_EXECUTABLE >> $ENVIRON_TMP_FILE
echo 'JYTHON_JAR='$JYTHON_JAR >> $ENVIRON_TMP_FILE

#
# Check whether we have simplejson available.
#
echo "Test if 'simplejson' is available to jython. Please wait..."
SIMPLEJSON_TEST=`$JYTHON_EXECUTABLE -c "import simplejson" 2>&1`
if [ $? == 1 ]; then
    echo "Could not find 'simplejson'. Installing now..."
    #
    # Looks like simplejson is not installed. Is 'easy_install'
    # available to us?
    #
    EASY_INSTALL=$JYTHON_HOME/bin/easy_install
    if [ ! -x $EASY_INSTALL ]; then
        # Need to install easy-install first.
        echo -e "\nFirst I need to install easy_install. Please wait..."
        $JYTHON_EXECUTABLE tools/ez_setup.py
        if [ -x $EASY_INSTALL ]; then
            echo "easy_install was installed successfully in" $EASY_INSTALL
        else
            error_report "Attempt to install easy_installed failed. Cannot continue..."
            exit 1
        fi
    fi
    #
    # Now we can install simplejson
    #
    echo "Installing simplejson for jython. Please wait..."
    $EASY_INSTALL simplejson
    SIMPLEJSON_TEST=`$JYTHON_EXECUTABLE -c "import simplejson" 2>&1`
    if [ $? == 1 ]; then
        error_report "Install of simplejson failed. Cannot continue..."
        exit 1
    fi
fi

echo "Ok. Jython found 'simplejson'."

#
# Setting the $GLU_HOME variable
#
GLU_HOME="`pwd`"
echo 'GLU_HOME='$GLU_HOME >> $ENVIRON_TMP_FILE

#
# Adding jython to our classpath
#
if [ -z $CLASSPATH ]; then
    CLASSPATH="$JYTHON_JAR:$GLU_HOME/src/java"
else
    CLASSPATH="$CLASSPATH:$JYTHON_JAR:$GLU_HOME/src/java"
fi
echo 'CLASSPATH='$CLASSPATH >> $ENVIRON_TMP_FILE

#
# Setting the $VERSION variable
#
VERSION=`cat $GLU_HOME/VERSION`
echo 'VERSION='$VERSION >> $ENVIRON_TMP_FILE

#
# Setting variables for the correct script names
#
echo 'COMPILE_SCRIPT='$GLU_HOME/$COMPILE_SCRIPT_DIR/$COMPILE_SCRIPT >> $ENVIRON_TMP_FILE
echo 'COMPILE_SCRIPT_NAME='$COMPILE_SCRIPT >> $ENVIRON_TMP_FILE
echo 'CTL_SCRIPT_NAME='$CTL_SCRIPT >> $ENVIRON_TMP_FILE
echo 'PID_FILE='$GLU_HOME/$PID_FILE >> $ENVIRON_TMP_FILE

# Check whether start-stop-daemon is available (on debian). If so,
# the gluctl script should use it start/stop the Glu server. If it's
# not available then we need to direct to a make-shift script that
# we have in our bin directory. The system start-stop-daemon is
# preferred when it's available.
EXEC_TEST=`builtin type -P start-stop-daemon`
if [ -z "$EXEC_TEST" ]; then
    # Need to use our own script
    echo 'START_STOP_DAEMON='$GLU_HOME/bin/glu_start_stop_daemon >> $ENVIRON_TMP_FILE
else
    # Can use the system 'start-stop-daemon' command
    echo 'START_STOP_DAEMON='start-stop-daemon >> $ENVIRON_TMP_FILE
fi

#
# Creating finalized control scripts. We are combining the bodies of those
# scripts (located in bin/*_frg) with the environment variables we have
# accumulated so far.
#
script_combiner $ENVIRON_TMP_FILE  $GLU_HOME/bin/frags/_ctl_frg        $GLU_HOME/$CTL_SCRIPT 
script_combiner $ENVIRON_TMP_FILE  $GLU_HOME/bin/frags/_compile_frg    $GLU_HOME/$COMPILE_SCRIPT_DIR/$COMPILE_SCRIPT

rm $ENVIRON_TMP_FILE

#
# Compiling all Java sources
#
$GLU_HOME/$COMPILE_SCRIPT_DIR/$COMPILE_SCRIPT all
if [ ?$ == 1 ]; then
    error_report "Compilation failed. Cannot continue..."
    exit 1
fi


#
# All done
#
echo -e "\n\nInstall completed successfully."
echo -e "\nThe '$CTL_SCRIPT' script was created in this directory. Please use"
echo -e "it to start, stop and restart the Glu server:\n"
echo "   % $CTL_SCRIPT start            # Start the glu server"
echo "   % $CTL_SCRIPT stop             # Stop a running Glu server"
echo "   % $CTL_SCRIPT restart          # Stops and restarts a Glu server"
echo -e "\nThank you for installing Glu.\n"
exit 0
