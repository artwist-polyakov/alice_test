#!/bin/sh


echo "Waiting for nginx 10 secs"
sleep 10

# Получение SSL-сертификатов
certbot certonly --webroot --webroot-path=/var/www/certbot --email artwist@yandex.ru --agree-tos --no-eff-email -d practix-cinema.ru -d www.practix-cinema.ru

echo "Waiting for certs 5 secs"
sleep 5

if [ ! -f /etc/letsencrypt/options-ssl-nginx.conf ]; then
    wget https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf -O /etc/letsencrypt/options-ssl-nginx.conf
fi

# Копирование ssl конфигурации в директории  nginx
cp /etc/nginx/support/practix-cinema.ru.ssl /etc/nginx/conf.d/practix-cinema.ru.ssl.conf
sleep 1
docker exec nginx nginx -s reload

# Обновление сертификатов каждые 12 часов
trap exit TERM; while :; do certbot renew; sleep 12h & wait ${!}; done;