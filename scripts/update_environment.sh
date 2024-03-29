#!/bin/bash

cd $(dirname $0)/..

# Compatibility logic for older Anaconda versions.
if [ "${CONDA_EXE} " == " " ]; then
    CONDA_EXE=$((find /opt/conda/bin/conda || find ~/anaconda3/bin/conda || \
        find /usr/local/anaconda3/bin/conda || find ~/miniconda3/bin/conda  || \
        find /root/miniconda/bin/conda || find ~/Anaconda3/Scripts/conda || \
        find $CONDA/bin/conda) 2>/dev/null)
fi

if [ "${CONDA_EXE}_" == "_" ]; then
    echo "Please install Anaconda w/ Python 3.7+ first"
    echo "See: https://www.anaconda.com/distribution/"
    exit 1
fi

CONDA_BIN=$(dirname ${CONDA_EXE})
ENV_FILE=support/environment.yml

if ${CONDA_EXE} env list | egrep -qe "^rogerthat"; then
    ${CONDA_EXE} env update -f $ENV_FILE
else
    ${CONDA_EXE} env create -f $ENV_FILE
fi

source "${CONDA_BIN}/activate" rogerthat


# Must be installed outside of environment wierdly
# pip install git+git://github.com/TheHolyRoger/atomacos.git@68215cc1cec6a59944b369ddf3178c7a1b25f3ea#egg=atomacos

pre-commit install
