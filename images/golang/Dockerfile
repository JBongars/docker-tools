
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/golang.dockerfile.j2
# AND RUN python ^/python/build.py
# ------------

FROM alpine:3.17.2

# Alpine Base
RUN apk update && apk upgrade

RUN apk add --no-cache  py3-pip \
                        git \
                        npm \
                        curl \
                        wget \
                        vim \
                        bash \
                        unzip \
                        jq \
                        python3

RUN apk add --no-cache zsh

RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

RUN npm i -g yarn

RUN rm -rf /var/cache/apk/*

ENV PATH="$PATH:/root/.local/bin"

WORKDIR /work

# Golang
RUN apk add --no-cache git make musl-dev go

# Configure Go
ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV PATH /go/bin:$PATH

RUN mkdir -p ${GOPATH}/src ${GOPATH}/bin