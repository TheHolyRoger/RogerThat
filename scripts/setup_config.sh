#!/bin/bash

cd $(dirname $0)/..

export PUID=$(id -u)
export PGID=$(id -g)

docker run -it --rm \
--volume "$(pwd)/configs:/configs" \
theholiestroger/rogerthat:latest \
./docker_start_setup_script.sh \
"$@"
