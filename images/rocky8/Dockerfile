
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/rocky8.dockerfile.j2
# AND RUN python ^/python/build.py rocky8
# ------------

FROM rockylinux:8.9

RUN yum install -y epel-release

# RHEL Base
RUN yum update -y  yum upgrade -y

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

RUN pip3 install --upgrade pip

# Image footer for quality of life improvements 

RUN yum install util-linux -y

RUN yum install zsh fish -y
# RUN git clone --recursive https://github.com/sorin-ionescu/prezto.git "${ZDOTDIR:-$HOME}/.zprezto"

COPY ./.zshrc /root/.zshrc
COPY ./config.fish /root/fish/config.fish
COPY ./onload.sh /root/onload.sh
RUN dos2unix /root/.zshrc
RUN dos2unix /root/onload.sh

RUN yum clean all
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /work    