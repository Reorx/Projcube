#!/bin/sh
mv /srv/nodemix_api/log/nginx.access.log /srv/nodemix_api/log/nginx.access_`date +%Y%m%d`.log
killall -s USR1 nginx
