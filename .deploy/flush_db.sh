#!/bin/bash
echo drop then create database ..
mysql --user="root" --password="h@*ML$A?R>L[w/e" -e 'drop database projcube;create database projcube;' 
echo done
echo jump to projcube/
cd ../projcube/
MYLS=$(pwd)
echo now at: $MYLS
echo rebuild database structure
python manage.py syncdb
