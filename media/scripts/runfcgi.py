#!/bin/sh
PROJDIR="/srv/nodemix_api/nodemix"
LOGDIR="/srv/nodemix_api/log"
PIDFILE="/srv/nodemix_api/log/main.pid"
cd $LOGDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi
cd $PROJDIR
exec python manage.py runfcgi host=127.0.0.1 port=8000 pidfile=${PIDFILE}
