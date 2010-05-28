#/bin/sh


pylint --rcfile=pylint.rc *.py | tee pylint.txt
