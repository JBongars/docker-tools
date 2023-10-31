
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/kube.dockerfile.j2
# AND RUN python ^/python/build.py kube
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

# Kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN chmod +x ./kubectl && mv ./kubectl /usr/local/bin
RUN echo "# kubectl code completion\nsource <(kubectl completion zsh)\n\n" >> ~/.zshrc
# Helm
RUN apk add --no-cache helm
# Kind
RUN curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.17.0/kind-linux-amd64
RUN chmod +x ./kind && mv ./kind /usr/local/bin/kind

# Image footer for quality of life improvements 

RUN apk add util-linux

RUN apk add zsh fish
# RUN git clone --recursive https://github.com/sorin-ionescu/prezto.git "${ZDOTDIR:-$HOME}/.zprezto"

COPY ./.zshrc /root/.zshrc
COPY ./onload.sh /root/onload.sh
RUN dos2unix /root/.zshrc
RUN dos2unix /root/onload.sh

RUN rm -rf /var/cache/apk/*
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /work