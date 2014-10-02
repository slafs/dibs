#!/bin/bash

python ./manage.py collectstatic -l --noinput && twistd -ny ./server.py
