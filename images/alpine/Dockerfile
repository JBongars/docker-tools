
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/alpine.dockerfile.j2
# AND RUN python ^/python/build.py alpine
# ------------

FROM alpine:3.18

# Alpine Base
RUN apk update && apk upgrade

RUN apk add --no-cache  build-base \
                        py3-pip \
                        git \
                        npm \
                        curl \
                        wget \
                        vim \
                        bash \
                        unzip \
                        jq \
                        python3 \
                        python3-dev \
                        dos2unix

RUN pip install --upgrade pip

# Image footer for quality of life improvements 

RUN apk add util-linux

RUN apk add zsh fish
# RUN git clone --recursive https://github.com/sorin-ionescu/prezto.git "${ZDOTDIR:-$HOME}/.zprezto"

COPY ./.zshrc /root/.zshrc
COPY ./onload.sh /root/onload.sh
RUN dos2unix /root/.zshrc
RUN dos2unix /root/onload.sh

RUN rm -rf /var/cache/apk/*
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /work