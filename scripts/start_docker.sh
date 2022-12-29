#!/bin/bash

if (( $EUID == 0 )) || (( $(id -u) == 0 )); then
    echo "Don't run RogerThat as sudo or root, it will cause permission errors. Exiting."
    exit
fi

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
    echo "${REV}-d${NORM}  --Run as Daemon." 1>&2
    echo "${REV}-c${NORM}  --Run with certbot renewing every 6 hours (Requires certificate to be set-up)." 1>&2
    echo -e \\n 1>&2
}

exit_abnormal() {                         # Function: Exit with error.
  usage
  exit 1
}

while getopts ":hndp" flag
do
    case "${flag}" in
        d) daemon=1;;
        p) dockerprune=1;;
        c) withcertbot=1;;
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
fi

if [ "${withcertbot} " == "1 " ]; then
    echo "Running with certbot."
    s_cb=" certbot"
fi

if [ "${daemon} " == "1 " ]; then
    echo "Running as daemon."
    s_dm=" -d"
fi

# Run setup script via docker
scripts/setup_config.sh -s

docker-compose up${s_dm} db rogerthat nginx${s_cb}

if [ "${daemon} " == "1 " ]; then
    scripts/setup_config.sh  --print-splash
fi
