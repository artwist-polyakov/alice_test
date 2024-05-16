#!/bin/sh

sleep 10

# Получение SSL-сертификатов
certbot certonly --webroot --webroot-path=/var/www/certbot --email artwist@yandex.ru --agree-tos --no-eff-email -d practix-cinema.ru -d www.practix-cinema.ru

# Копирование ssl конфигурации в директории  nginx
cp /etc/nginx/support/practix-cinema.ru.ssl /etc/nginx/conf.d/practix-cinema.ru.ssl.conf

docker restart nginx

# Обновление сертификатов каждые 12 часов
trap exit TERM; while :; do certbot renew; sleep 12h & wait ${!}; done;