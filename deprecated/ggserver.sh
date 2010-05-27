#/bin/sh

clear
echo "executing server "
echo "-----------------"
echo

export PYTHONPATH="./dmvc"
#python  -m cProfile -o ggserver.prof  gg/ggserver
python gg/ggserver 
