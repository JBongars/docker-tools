#!/bin/bash

if [ -z $NGROK_TOKEN ]; then
    echo "Please set 'NGROK_TOKEN' environment variable."
    exit 2
fi

if [ -z $NGROK_PORT ]; then
    echo "Please set 'NGROK_PORT' environment variable."
    exit 2
fi

if [ -z $NGROK_PROTOCOL ]; then
    NGROK_PROTOCOL="http"
fi

ngrok config add-authtoken $NGROK_TOKEN

ngrok $NGROK_PROTOCOL $NGROK_PORT