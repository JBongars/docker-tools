
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/lua.dockerfile.j2
# AND RUN python ^/python/build.py lua
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

RUN apk add build-base readline-dev curl

WORKDIR /tmp/lua

# Lua source
ENV LUA_VERSION 5.4.6
# RUN curl -s https://www.lua.org/ftp/ | grep -o 'lua-[0-9]\+\.[0-9]\+\.[0-9]\+' | sort -V | tail -n1 | tee lua_version.txt
RUN curl -Lo lua.tar.gz "https://www.lua.org/ftp/lua-${LUA_VERSION}.tar.gz" && \
    tar -xzvf lua.tar.gz && \
    rm lua.tar.gz

RUN mv "lua-$LUA_VERSION" lua && \
    cd lua && \
    make linux test && \
    make install

# LuaRocks source
ENV LUAROCKS_VERSION 3.9.2
# RUN curl -s https://luarocks.org/releases/ | grep -o 'luarocks-[0-9]\+\.[0-9]\+\.[0-9]\+' | sort -V | tail -n1 | tee luarocks_version.txt
RUN curl -Lo luarocks.tar.gz "https://luarocks.org/releases/luarocks-${LUAROCKS_VERSION}.tar.gz" && \
    tar -xzvf luarocks.tar.gz && \
    rm luarocks.tar.gz

RUN mv "luarocks-$LUAROCKS_VERSION" luarocks && \
    cd luarocks && \
    ./configure && \
    make && \
    make install

# Install the lua-json package using LuaRocks
RUN luarocks install lua-json

# Image footer for quality of life improvements 

RUN apk add util-linux

RUN apk add zsh fish
# RUN git clone --recursive https://github.com/sorin-ionescu/prezto.git "${ZDOTDIR:-$HOME}/.zprezto"

COPY ./.zshrc /root/.zshrc
COPY ./config.fish /root/fish/config.fish
COPY ./onload.sh /root/onload.sh
RUN dos2unix /root/.zshrc
RUN dos2unix /root/onload.sh

RUN rm -rf /var/cache/apk/*
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /work