FROM certbot/certbot

RUN apk add --no-cache curl
COPY certbot.sh /certbot.sh

RUN chmod +x /certbot.sh

ENTRYPOINT ["/certbot.sh"]