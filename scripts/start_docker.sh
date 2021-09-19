#!/bin/bash

cd $(dirname $0)/..

while getopts ":ndp" flag
do
    case "${flag}" in
        n) nostart=1;;
        d) dontbuild=1;;
        p) dockerprune=1;;
    esac
done

if [ "${dockerprune} " == "1 " ]; then
    echo "Pruning docker."
    docker system prune
fi

if [ "${dontbuild} " == "1 " ]; then
    echo "Skipping build."
else
    docker build -t rogerthat:latest .
fi

# Run setup script via docker
scripts/start_docker_setup_script.sh -s

if [ "${nostart} " == "1 " ]; then
    echo "Skipping start."
else
    docker compose up
fi
