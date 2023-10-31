
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/ngrok.dockerfile.j2
# AND RUN python ^/python/build.py ngrok
# ------------

FROM alpine:3.18

RUN apk add curl tar bash

WORKDIR /ngrok

RUN curl -L https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -o ngrok.tgz
RUN tar -xvf ngrok.tgz
RUN mv ngrok /usr/local/bin && chmod +x /usr/local/bin/ngrok
RUN rm ngrok.tgz

COPY ./entrypoint.sh /ngrok/entrypoint.sh

CMD ["/ngrok/entrypoint.sh"]