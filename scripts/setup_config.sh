#!/bin/bash

cd $(dirname $0)/..

export PUID=$(id -u)
export PGID=$(id -g)

mkdir -p ./data/db
mkdir -p ./data/certbot/certs
mkdir -p ./data/certbot/www

chown -R $PUID:$PGID ./data

docker run -it --rm \
--volume "$(pwd)/configs:/configs" \
theholiestroger/rogerthat:latest \
./docker_start_setup_script.sh \
"$@"
