#/bin/sh

clear
echo "executing client "
echo "-----------------"
echo

export PYTHONPATH="./dmvc"
python gg/genteguada -e remoto
