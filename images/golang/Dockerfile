
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/golang.dockerfile.j2
# AND RUN python ^/python/build.py golang
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


ARG GO_VERSION=1.21.3

RUN echo "@testing https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk update

# Golang
RUN apk add --no-cache git make musl-dev@testing
# RUN apk add --no-cache go@testing
RUN curl -L "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz" -o "/tmp/go.tar.gz"
RUN mkdir -p /go && tar -C / -xzf /tmp/go.tar.gz && rm /tmp/go.tar.gz

# Configure Go
# ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV PATH /go/bin:$PATH

# Dev tools
RUN go install golang.org/x/tools/gopls@latest
RUN go install github.com/go-delve/delve/cmd/dlv@latest
RUN go install github.com/ramya-rao-a/go-outline@latest
RUN go install github.com/uudashr/gopkgs/v2/cmd/gopkgs@latest

RUN mkdir -p ${GOPATH}/src ${GOPATH}/bin

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