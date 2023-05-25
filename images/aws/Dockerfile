
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

RUN apk add --no-cache zsh

RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

COPY ./.zshrc /root/.zshrc
COPY ./onload.sh /root/onload.sh

RUN npm i -g yarn

RUN rm -rf /var/cache/apk/*

ENV PATH="$PATH:/root/.local/bin"

WORKDIR /work

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
ARG TERRAFORM_VERSION=1.3.9

RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN mv terraform /usr/bin/terraform

RUN apk add --no-cache terraform
# Ansible
RUN python3 -m pip install --user ansible
RUN python3 -m pip install --user argcomplete