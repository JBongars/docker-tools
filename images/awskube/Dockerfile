
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/awskube.dockerfile.j2
# AND RUN python ^/python/build.py awskube
# ------------

FROM docker:23.0.1-dind-alpine3.17

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

RUN npm i -g yarn

RUN rm -rf /var/cache/apk/*

ENV PATH="$PATH:/root/.local/bin"

WORKDIR /work

# Kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN chmod +x ./kubectl && mv ./kubectl /usr/local/bin
RUN echo "# kubectl code completion\nsource <(kubectl completion zsh)\n\n" >> ~/.zshrc
# Helm
RUN apk add --no-cache helm
# Kind
RUN curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.17.0/kind-linux-amd64
RUN chmod +x ./kind && mv ./kind /usr/local/bin/kind

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
ARG TERRAFORM_VERSION=1.4.6

RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN mv terraform /usr/bin/terraform

RUN apk add --no-cache terraform
# Ansible
RUN python3 -m pip install --user ansible
RUN python3 -m pip install --user argcomplete
RUN curl -L https://github.com/cli/cli/releases/download/v2.30.0/gh_2.30.0_linux_386.tar.gz > ghcli.tar.gz
RUN tar -xvf ghcli.tar.gz 
# RUN ls
# RUN mv gh_2.30.0_linux_386/bin/gh /bin/gh

RUN echo "alias ghlogin='gh auth login --with-token < /root/.git-credentials/.accesstoken'" >> /root/.zshrc

WORKDIR /work