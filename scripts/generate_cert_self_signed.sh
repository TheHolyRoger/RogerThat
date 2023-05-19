#!/bin/bash


cd $(dirname $0)/..

DOCKER_BIN=$(scripts/find_docker.sh)

$DOCKER_BIN run --rm --entrypoint "/bin/sh /generate_self_signed_cert.sh" certbot
