#!/bin/sh

# Получение SSL-сертификатов
certbot certonly --webroot --webroot-path=/var/www/certbot --artwist@yandex.ru --agree-tos --no-eff-email -d practix-cinema.ru -d www.practix-cinema.ru

# Обновление сертификатов каждые 12 часов
trap exit TERM; while :; do certbot renew; sleep 12h & wait ${!}; done;