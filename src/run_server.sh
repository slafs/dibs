#!/bin/bash

python ./manage.py collectstatic --noinput && twistd -ny ./server.py
