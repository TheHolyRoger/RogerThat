#!/bin/bash

if (( $EUID == 0 )) || (( $(id -u) == 0 )); then
    echo "Don't run RogerThat as sudo or root, it will cause permission errors. Exiting."
    exit
fi

cd $(dirname $0)/..

export PUID=$(id -u)
export PGID=$(id -g)

mkdir -p ./data/db
mkdir -p ./data/certbot/certs
mkdir -p ./data/certbot/www

docker run -it --rm \
--volume "$(pwd)/configs:/configs" \
"theholiestroger/rogerthat:${ROGERTHAT_IMG_NAME:-mqtt}" \
./docker_start_setup_script.sh \
"$@"
