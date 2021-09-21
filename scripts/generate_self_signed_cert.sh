#!/bin/bash

cd $(dirname $0)/..

export PUID=$(id -u)
export PGID=$(id -g)

docker run -it --rm  --volume "$(pwd)/certs:/certs" theholiestroger/rogerthat:latest ./generate_self_signed_cert.sh
