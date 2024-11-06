#!/bin/sh
if [ -z ${ENV_CONFIG} ]; 
    then echo "ENV_CONFIG is unset"; 
    exit 1
else 
    echo "ENV_CONFIG is set to '$ENV_CONFIG'"; 
    echo "Starting my application..."
    uwsgi uwsgi.ini
    fi
