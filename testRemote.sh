#/bin/sh

clear
echo "executing client side tests"
echo "---------------------------"
echo

export PYTHONPATH="./dmvc"
python dmvc/test/testRemote.py
