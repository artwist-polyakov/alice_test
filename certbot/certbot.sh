#!/bin/sh

certbot certonly --webroot --webroot-path=/var/www/certbot --email artwist@yandex.ru --agree-tos --no-eff-email -d practix-cinema.ru -d www.practix-cinema.ru
trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;