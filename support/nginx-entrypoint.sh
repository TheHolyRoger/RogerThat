#!/usr/bin/env sh
set -eu

if [ -d "/etc/nginx/rogerthat_certs" ] && [ -f "/etc/nginx/rogerthat_certs/server.key" ]; then
	envsubst '${HOSTNAME} ${API_PORT}' < /etc/nginx/conf.d/ssl.conf.template > /etc/nginx/conf.d/default.conf
else
	envsubst '${HOSTNAME} ${API_PORT}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
fi

exec "$@"