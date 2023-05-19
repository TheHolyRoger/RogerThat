#!/bin/bash

cd $(dirname $0)/

# Compatibility logic for older Anaconda versions.
if [ "${CONDA_EXE} " == " " ]; then
    CONDA_EXE=$((find /opt/conda/bin/conda || find ~/anaconda3/bin/conda || \
        find /usr/local/anaconda3/bin/conda || find ~/miniconda3/bin/conda  || \
        find /root/miniconda/bin/conda || find ~/Anaconda3/Scripts/conda) 2>/dev/null)
fi

if [ "${CONDA_EXE}_" == "_" ]; then
    echo "Please install Anaconda w/ Python 3.7+ first"
    echo "See: https://www.anaconda.com/distribution/"
    exit 1
fi

CONDA_BIN=$(dirname ${CONDA_EXE})
source "${CONDA_BIN}/activate" rogerthat

~/wait-for-it.sh -t 40 db:5432

scripts/setup.py -s

sleep 10

killpg(){
  echo "Beginning RogerThat Shutdown."
  rogerthat_pid=`cat .rogerthat.pid`
  echo "Killing PID $rogerthat_pid."
  kill -15 "$rogerthat_pid"
  while [ "$(ps -ax | grep [p]ython)" != "" ]; do
    sleep 1s
  done
  echo "Finished Shutdown."
  exit 0
}

trap killpg INT TERM

bin/start_rogerthat.py &

while :; do
    sleep 1s
done

exit 0
