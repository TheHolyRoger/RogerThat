#!/bin/bash
set -e

cd $(dirname $0)/../..

DOCKER_BIN=$(scripts/find_docker.sh)

SCRIPT=`basename ${BASH_SOURCE[0]}`

NORM=`tput sgr0`
BOLD=`tput bold`
REV=`tput smso`

usage() {
    echo -e \\n"Help documentation for ${BOLD}${SCRIPT}.${NORM}"\\n 1>&2
    echo -e "${REV}Usage:${NORM} ${BOLD}$0 [ -n ] [ -d ] [ -p ]${NORM}"\\n 1>&2
    echo -e "Use the following optional switches."\\n 1>&2
    echo "${REV}-n${NORM}  --Skip starting." 1>&2
    echo "${REV}-d${NORM}  --Don't Build." 1>&2
    echo "${REV}-p${NORM}  --Prune docker." 1>&2
    echo -e \\n 1>&2
}

exit_abnormal() {                         # Function: Exit with error.
  usage
  exit 1
}

while getopts ":hndp" flag
do
    case "${flag}" in
        n) nostart=1;;
        d) dontbuild=1;;
        p) dockerprune=1;;
        h) exit_abnormal;;
        \?) exit_abnormal;;
    esac
done

if [[ -n "$IS_WSL" || -n "$WSL_DISTRO_NAME" ]]; then
    echo "Running on WSL."
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Running on OSX."
else
    export PUID=$(id -u)
    export PGID=$(id -g)
    echo "Running on the good stuff as UID ${PUID} GID ${PGID}"
fi

if [ "${dockerprune} " == "1 " ]; then
    echo "Pruning docker."
    docker system prune -f
    docker rmi theholiestroger/nginx-iptables:latest || true
    docker rmi "theholiestroger/rogerthat:${ROGERTHAT_IMG_NAME:-latest}" || true
fi

if [ "${dontbuild} " == "1 " ]; then
    echo "Skipping build."
else
    docker image prune -f
    $DOCKER_BIN build --progress plain
fi

echo "Calling setup script"

# Run setup script via docker
scripts/setup_config.sh -s

if [ "${nostart} " == "1 " ]; then
    echo "Skipping start."
else
    $DOCKER_BIN up db rogerthat nginx
fi
