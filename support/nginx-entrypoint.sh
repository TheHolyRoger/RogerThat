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

http_port=8080
https_port=8443

if [ "${ADD_CLOUDFLARE_IPTABLES:-}" != "" ]; then
  iptables="/usr/sbin/iptables"

  host_ip=`/sbin/ip route|awk '/default/ { print $3 }'`

  $iptables -I INPUT -p tcp -m multiport --dports "$http_port,$https_port" -j DROP
  for i in `curl -s https://www.cloudflare.com/ips-v4`;\
    do $iptables -I INPUT -p tcp -m multiport --dports "$http_port,$https_port" -s $i -j ACCEPT;\
  done
  $iptables -I INPUT -p tcp -m multiport --dports "$http_port,$https_port" -s "$host_ip" -j ACCEPT
fi

# Reload every 6h in background
while :; do sleep 6h & wait $!; nginx -s reload; done &

exec "$@"
