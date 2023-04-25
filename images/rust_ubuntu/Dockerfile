
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/rust_ubuntu.dockerfile.j2
# AND RUN python ^/python/build.py rust_ubuntu
# ------------

FROM ubuntu:22.04

# ubuntu Base
RUN apt-get -y update && apt-get -y upgrade

RUN apt -y install software-properties-common
RUN apt -y install apt-transport-https ca-certificates
RUN apt -y install python3 python3-pip
RUN apt -y install git curl vim zsh unzip jq

RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
COPY ./.zshrc /root/.zshrc

RUN apt -y upgrade -y && apt-get -y autoremove -y && apt-get -y clean -y

ENV PATH="$PATH:/root/.local/bin"

WORKDIR /work

RUN apt-get -y install build-essential

WORKDIR /rust

RUN curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -o rustup.sh
RUN chmod +x rustup.sh
RUN ./rustup.sh -y -v
RUN chmod +x $HOME/.cargo/env
RUN $HOME/.cargo/env

WORKDIR /work
RUN rm -rf /rust
