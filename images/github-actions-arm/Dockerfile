
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/github-actions-arm.dockerfile.j2
# AND RUN python ^/python/build.py github-actions-arm
# ------------


# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/github-actions-arm.dockerfile.j2
# AND RUN python ^/python/build.py github-actions-arm
# ------------

FROM ubuntu:22.04

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install libkrb5-3 zlib1g curl tar jq python3 python3-pip git bash

RUN  mkdir actions-runner && cd actions-runner
RUN chmod 700 /actions-runner
WORKDIR /actions-runner

# Github Actions Runner
# ---------------------------------------------
RUN curl -O -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-arm64-2.311.0.tar.gz
RUN  echo "5d13b77e0aa5306b6c03e234ad1da4d9c6aa7831d26fd7e37a3656e77153611e  actions-runner-linux-arm64-2.311.0.tar.gz" | sha256sum -c
RUN tar xzf ./actions-runner-linux-arm64-2.311.0.tar.gz
RUN /bin/bash ./bin/installdependencies.sh

# Github CLI
# ---------------------------------------------
RUN curl -L https://github.com/cli/cli/releases/download/v2.39.1/gh_2.39.1_linux_arm64.tar.gz -o ghcli.tar.gz
RUN tar -xvf ghcli.tar.gz 
RUN cp ./gh_2.39.1_linux_arm64/bin/gh /bin/gh

# Sudo User for Github Actions Runner
# ---------------------------------------------
RUN apt-get -y install sudo
RUN useradd -m runner && echo "runner:runner" | chpasswd && adduser runner sudo
# don't prompt for password when using sudo
RUN echo "runner ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/runner
RUN chmod +x /actions-runner/* && chown -R runner:runner /actions-runner

# Customize environment
# ---------------------------------------------
RUN apt-get -y install zip dos2unix parallel
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN sudo ./aws/install

USER runner

ENV GITHUB_PAT_TOKEN ""
ENV GITHUB_REPO_URL ""
ENV GITHUB_TOKEN ""

COPY ./init.sh /actions-runner/init.sh

ENTRYPOINT ["bash", "-c", "/actions-runner/init.sh"]