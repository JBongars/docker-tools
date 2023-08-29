
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/aws.dockerfile.j2
# AND RUN python ^/python/build.py aws
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
                        python3-dev \
                        dos2unix

RUN pip install --upgrade pip

RUN apk add --no-cache zsh fish
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

COPY ./.zshrc /root/.zshrc
COPY ./onload.sh /root/onload.sh
RUN dos2unix /root/.zshrc
RUN dos2unix /root/onload.sh

RUN apk add nvim
# add any neovim configuration here

RUN apk add build-base readline-dev curl

WORKDIR /tmp/lua

# Lua source
ENV LUA_VERSION 5.4.6
# RUN curl -s https://www.lua.org/ftp/ | grep -o 'lua-[0-9]\+\.[0-9]\+\.[0-9]\+' | sort -V | tail -n1 | tee lua_version.txt
RUN curl -Lo lua.tar.gz "https://www.lua.org/ftp/lua-$LUA_VERSION.tar.gz" && \
    tar -xzvf lua.tar.gz && \
    rm lua.tar.gz

RUN mv "lua-$LUA_VERSION" lua && \
    cd lua && \
    make linux test && \
    make install

# LuaRocks source
ENV LUAROCKS_VERSION 3.9.2
# RUN curl -s https://luarocks.org/releases/ | grep -o 'luarocks-[0-9]\+\.[0-9]\+\.[0-9]\+' | sort -V | tail -n1 | tee luarocks_version.txt
RUN curl -Lo luarocks.tar.gz "https://luarocks.org/releases/luarocks-$LUAROCKS_VERSION.tar.gz" && \
    tar -xzvf luarocks.tar.gz && \
    rm luarocks.tar.gz

RUN mv "luarocks-$LUAROCKS_VERSION" luarocks && \
    cd luarocks && \
    ./configure && \
    make && \
    make install

# Install the lua-json package using LuaRocks
RUN luarocks install lua-json

RUN npm i -g yarn

RUN rm -rf /var/cache/apk/*

ENV PATH="$PATH:/root/.local/bin"

WORKDIR /work

WORKDIR /tmp

# AWS
RUN apk add --no-cache \
        python3 \
        py3-pip \
    && pip3 install --upgrade pip \
    && pip3 install --no-cache-dir \
        awscliv2 \
    && rm -rf /var/cache/apk/*
    
RUN apk add python3 py3-pip gcc musl-dev python3-dev
RUN pip install awscli aws-sam-cli
RUN sam --version
# Terraform
ARG TERRAFORM_VERSION=1.5.2

RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN mv terraform /usr/bin/terraform
COPY ./vault.tar.gz /tmp/vault.tar.gz
RUN tar -xzf /tmp/vault.tar.gz -C /tmp/ && rm /tmp/vault.tar.gz
RUN mv /tmp/vault/vault /usr/local/bin/vault && rm -rf /tmp/vault
# Ansible
RUN python3 -m pip install --user ansible
RUN python3 -m pip install --user argcomplete
RUN curl -L https://github.com/cli/cli/releases/download/v2.30.0/gh_2.30.0_linux_386.tar.gz > ghcli.tar.gz
RUN tar -xvf ghcli.tar.gz 
RUN cp ./gh_2.30.0_linux_386/bin/gh /bin/gh

RUN echo "alias ghlogin='gh auth login --with-token < /root/.git-credentials/.accesstoken'" >> /root/.zshrc

WORKDIR /work