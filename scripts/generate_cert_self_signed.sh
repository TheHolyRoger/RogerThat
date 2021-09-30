#!/bin/bash


cd $(dirname $0)/..

docker-compose run --rm --entrypoint "/bin/sh /generate_self_signed_cert.sh" certbot
