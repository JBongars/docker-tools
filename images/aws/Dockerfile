
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/aws.dockerfile.j2
# AND RUN python ^/python/build.py aws
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
ARG TERRAFORM_VERSION=1.6.2

RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN mv terraform /usr/bin/terraform
# Install hashicorp Packer

RUN curl -L https://releases.hashicorp.com/packer/1.10.0/packer_1.10.0_linux_amd64.zip -o /tmp/packer.zip && \
    unzip /tmp/packer.zip -d /usr/local/bin && \
    rm /tmp/packer.zip
    
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