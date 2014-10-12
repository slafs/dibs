#!/bin/bash

OPT=${1:-"--dev"}

if [ "$OPT" == "--dev" ]; then
    TWISTD_OPTIONS="-n"
    COLLECTSTATIC_OPTIONS="-l --noinput"
else
    TWISTD_OPTIONS=""
    COLLECTSTATIC_OPTIONS="--noinput"
fi

cd ./src

python ./manage.py collectstatic ${COLLECTSTATIC_OPTIONS} && twistd ${TWISTD_OPTIONS} -y ./server.py
