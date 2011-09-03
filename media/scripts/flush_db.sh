#!/bin/bash
echo drop then create database..
mysql --user=remote --password=pilved -e 'drop database nmadmin;create database nmadmin;' 
echo done
echo jump to nodemix/
cd ../../
MYLS=$(pwd)
echo now at: $MYLS
echo rebuild database structure
python manage.py syncdb
