#!/bin/sh

certbot certonly --webroot --webroot-path=/var/www/certbot --email your-email@example.com --agree-tos --no-eff-email -d practix-cinema.ru -d www.practix-cinema.ru
trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;