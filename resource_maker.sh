#!/bin/bash

#
# A small tool to help create new resources.
#
# Usage: resource_maker.sh <server_url>
#

if [ -z "$1" ]; then
    echo "Usage: resource_maker.sh <server_url>"
    exit 1
fi

cd src/python
pexec="python"
EXEC_TEST=`builtin type -P $pexec`
if [ -z "$EXEC_TEST" ]; then
    pexec="jython"
fi
$pexec resource_maker.py "$1"

