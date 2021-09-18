#!/bin/bash

cd $(dirname $0)/..

openssl req -newkey rsa:2048 -nodes -keyout certs/server.key -x509 -days 365 -out certs/server.crt
