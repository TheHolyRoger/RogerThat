#!/bin/bash

cd $(dirname $0)/..

docker run -it --rm \
--volume "$(pwd)/configs:/configs" \
rogerthat:latest \
/home/rogerthat/start_docker_setup_script.sh \
"$@"
