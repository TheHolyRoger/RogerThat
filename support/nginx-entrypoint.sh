#!/usr/bin/env sh
set -eu

envsubst '${HOSTNAME} ${API_PORT}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

exec "$@"