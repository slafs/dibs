#!/bin/bash

OPT=${1:-"--nodaemon"}

if [ "$OPT" == "--nodaemon" ]; then
    DAEMON=n
else
    DAEMON=""
fi


python ./manage.py collectstatic -l --noinput && twistd -${DAEMON}y ./server.py
