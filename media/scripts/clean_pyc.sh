#!/bin/bash
echo jumping to project core dir ...
cd ../../../
MYLS=$(pwd)
echo now at: $MYLS
echo refreshing..
find nmadmin/ -name '*.pyc' -exec rm {} \;
echo finish refreshing
MYFIND=$(find nmadmin/ -name '*.pyc')
echo check if any .pyc left: $MYFIND
