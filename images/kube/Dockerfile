
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