
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/rocky.dockerfile.j2
# AND RUN python ^/python/build.py rocky
# ------------

FROM fedora:41

# RHEL Base
RUN yum update -y  yum upgrade -y

RUN yum install -y epel-release

RUN yum install -y \
    python3 \
    python3-pip \
    git \
    npm \
    curl \
    wget \
    vim \
    bash \
    unzip \
    jq \
    dos2unix

RUN pip install --upgrade pip

# Image footer for quality of life improvements 

RUN yum install util-linux -y

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