#!/bin/bash

domains="${HOSTNAME}"
data_path="/etc/letsencrypt"

if [ "$domains" == "localhost" ]; then
  echo "ERROR: Cannot use localhost with letsencrypt."
  exit 0
fi

rm -Rf "$data_path/live/$domains" && \
rm -Rf "$data_path/archive/$domains" && \
rm -Rf "$data_path/renewal/$domains.conf"

staging="${STAGING:-0}" # Set to 1 if you're testing your setup to avoid hitting request limits
# Enable staging mode if needed
if [ $staging != "0" ]; then staging_arg="--staging"; fi

certbot certonly --webroot -w /var/www/certbot \
$staging_arg \
--register-unsafely-without-email \
-d "${HOSTNAME}" \
--rsa-key-size 4096 \
--agree-tos \
--force-renewal
