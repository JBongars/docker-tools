#!/bin/bash

if [ -z $NGROK_TOKEN ]; then
    echo "Please set 'NGROK_TOKEN' environment variable."
    exit 2
fi

if [ -z $NGROK_PORT ]; then
    echo "Please set 'NGROK_TOKEN' environment variable."
    exit 2
fi

ngrok config add-authtoken $NGROK_TOKEN
ngrok tcp $NGROK_PORT