
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/node.dockerfile.j2
# AND RUN python ^/python/build.py node
# ------------

FROM alpine:3.17.2

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
                        python3-dev

RUN pip install --upgrade pip

RUN apk add --no-cache zsh

RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

COPY ./.zshrc /root/.zshrc

RUN npm i -g yarn

RUN rm -rf /var/cache/apk/*

ENV PATH="$PATH:/root/.local/bin"

WORKDIR /work

RUN apk add --no-cache nodejs npm
RUN npm i -g yarn