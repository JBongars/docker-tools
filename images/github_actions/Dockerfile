
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/github_actions.dockerfile.j2
# AND RUN python ^/python/build.py
# ------------

FROM ubuntu:22.04

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install libkrb5-3 zlib1g curl tar 

RUN  mkdir actions-runner && cd actions-runner
RUN chmod 700 /actions-runner
WORKDIR /actions-runner

RUN curl -o actions-runner-linux-x64-2.301.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.301.1/actions-runner-linux-x64-2.301.1.tar.gz
RUN  echo "3ee9c3b83de642f919912e0594ee2601835518827da785d034c1163f8efdf907  actions-runner-linux-x64-2.301.1.tar.gz" | sha256sum -c
RUN  tar xzf ./actions-runner-linux-x64-2.301.1.tar.gz
RUN /bin/bash ./bin/installdependencies.sh

RUN adduser runner
RUN chmod +x /actions-runner/* && chown -R runner:runner /actions-runner

USER runner

ENV GITHUB_REPO_URL ""
ENV GITHUB_TOKEN ""

CMD ["/bin/sh", "-c", "./config.sh --url $GITHUB_REPO_URL --token $GITHUB_TOKEN --unattended && ./run.sh"]