#!/bin/bash


cd $(dirname $0)/..

echo "### Begin generating certificate"

DOCKER_BIN=$(scripts/find_docker.sh)

scripts/setup_config.sh -s

$DOCKER_BIN stop

echo "### Downloading SSL params ..."
$DOCKER_BIN run --rm --entrypoint "/bin/sh /letsencrypt_download_params.sh" certbot


echo "### Starting nginx ..."
$DOCKER_BIN up --force-recreate -d nginx
echo


echo "### Requesting Let's Encrypt certificate ..."
$DOCKER_BIN run --rm --entrypoint "/bin/sh /letsencrypt_generate.sh" certbot

echo "### Stopping nginx ..."
$DOCKER_BIN stop nginx

echo "### Finished generating certificate you can now start RogerThat!"
