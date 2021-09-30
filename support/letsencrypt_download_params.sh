#!/bin/bash

domains="${HOSTNAME}"
data_path="/etc/letsencrypt"


if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended TLS parameters ..."
  mkdir -p "$data_path/conf"
  wget -O - https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
  wget -O - https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
  echo
fi

rm -Rf "$data_path/live/$domains" && \
rm -Rf "$data_path/archive/$domains" && \
rm -Rf "$data_path/renewal/$domains.conf"
