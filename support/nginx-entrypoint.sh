#!/usr/bin/env sh
set -eu

if [ -d "/etc/letsencrypt/live/${HOSTNAME}" ] && \
	[ -f "/etc/letsencrypt/live/${HOSTNAME}/fullchain.pem" ] && \
	[ -f "/etc/letsencrypt/live/${HOSTNAME}/privkey.pem" ] && \
	[ -f "/etc/letsencrypt/conf/options-ssl-nginx.conf" ] && \
	[ -f "/etc/letsencrypt/conf/ssl-dhparams.pem" ]
then
	envsubst '${HOSTNAME} ${API_PORT}' < /etc/nginx/conf.d/ssl.conf.template > /etc/nginx/conf.d/default.conf
else
	envsubst '${HOSTNAME} ${API_PORT}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
fi

exec "$@"
