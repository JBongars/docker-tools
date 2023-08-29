
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/alpine.dockerfile.j2
# AND RUN python ^/python/build.py alpine
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