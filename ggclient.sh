#/bin/sh

clear
echo "executing client "
echo "-----------------"
echo

export PYTHONPATH="./dmvc"
#python gg/genteguada -i 192.168.0.104
python gg/genteguada -i 127.0.0.1

