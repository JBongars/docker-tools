
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/github_actions.dockerfile.j2
# AND RUN python ^/python/build.py github_actions
# ------------

FROM ubuntu:22.04

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install libkrb5-3 zlib1g curl tar jq python3 python3-pip git bash

RUN  mkdir actions-runner && cd actions-runner
RUN chmod 700 /actions-runner
WORKDIR /actions-runner

# Github Actions Runner
# ---------------------------------------------
RUN curl -o actions-runner-linux-x64-2.301.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.301.1/actions-runner-linux-x64-2.301.1.tar.gz
RUN  echo "3ee9c3b83de642f919912e0594ee2601835518827da785d034c1163f8efdf907  actions-runner-linux-x64-2.301.1.tar.gz" | sha256sum -c
RUN  tar xzf ./actions-runner-linux-x64-2.301.1.tar.gz
RUN /bin/bash ./bin/installdependencies.sh

# Github CLI
# ---------------------------------------------
RUN curl -L https://github.com/cli/cli/releases/download/v2.30.0/gh_2.30.0_linux_386.tar.gz > ghcli.tar.gz
RUN tar -xvf ghcli.tar.gz 
RUN cp ./gh_2.30.0_linux_386/bin/gh /bin/gh

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
RUN curl -L "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" # AWS CLI
RUN unzip /tmp/awscliv2.zip -d /tmp
RUN sudo /tmp/aws/install

USER runner

ENV GITHUB_PAT_TOKEN ""
ENV GITHUB_REPO_URL ""
ENV GITHUB_TOKEN ""

COPY ./init.sh /actions-runner/init.sh

ENTRYPOINT ["bash", "-c", "/actions-runner/init.sh"]