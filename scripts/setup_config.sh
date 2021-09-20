#!/bin/bash

cd $(dirname $0)/..

docker run -it --rm \
--volume "$(pwd)/configs:/configs" \
theholiestroger/rogerthat:latest \
/home/rogerthat/docker_start_setup_script.sh \
"$@"
