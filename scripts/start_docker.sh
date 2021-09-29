#!/bin/bash

cd $(dirname $0)/..

SCRIPT=`basename ${BASH_SOURCE[0]}`

NORM=`tput sgr0`
BOLD=`tput bold`
REV=`tput smso`

usage() {
    echo -e \\n"Help documentation for ${BOLD}${SCRIPT}.${NORM}"\\n 1>&2
    echo -e "${REV}Usage:${NORM} ${BOLD}$0 [ -p ]${NORM}"\\n 1>&2
    echo -e "Use the following optional switches."\\n 1>&2
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
        p) dockerprune=1;;
        h) exit_abnormal;;
        \?) exit_abnormal;;
    esac
done

export PUID=$(id -u)
export PGID=$(id -g)

if [ "${dockerprune} " == "1 " ]; then
    echo "Pruning docker."
    docker system prune -f
fi

# Run setup script via docker
scripts/setup_config.sh -s

docker-compose up db rogerthat nginx
