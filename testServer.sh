#/bin/sh

# $Id$:

clear
echo "executing server side tests"
echo "---------------------------"
echo

export PYTHONPATH="./dmvc"
python dmvc/test/testServer
