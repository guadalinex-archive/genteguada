#/bin/sh

clear
echo "executing client "
echo "-----------------"
echo

export PYTHONPATH="./dmvc"
python gg/genteguada -i 192.168.0.33 -u pepe2 -p 12345
