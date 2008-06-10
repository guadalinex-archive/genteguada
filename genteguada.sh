#/bin/sh

clear
echo "executing genteguada game "
echo "--------------------------"
echo

export PYTHONPATH="./dmvc"
#python -m cProfile -o genteguada.prof gg/genteguada 
python gg/genteguada 
