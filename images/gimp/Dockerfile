FROM debian:buster-slim

RUN apt-get -y update && apt-get -y upgrade

RUN apt-get -y install pixmap

RUN apt-get update && apt-get install -y \
    gimp \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "gimp" ]