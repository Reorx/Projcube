#!/bin/bash
echo jumping to upper dir \(where can find project core code \) ..
cd ../../
MYLS=$(pwd)
echo now at: $MYLS
echo refreshing..
find projcube/ -name '*.pyc' -exec rm {} \;
echo finish refreshing
MYFIND=$(find projcube/ -name '*.pyc')
echo check if any .pyc left: $MYFIND
