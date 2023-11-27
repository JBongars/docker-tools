
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/postman.dockerfile.j2
# AND RUN python ^/python/build.py postman
# ------------

FROM ubuntu:latest

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install curl tar 

RUN mkdir /postman
WORKDIR /postman

RUN curl -o postman-agent.tar.gz -L https://dl.pstmn.io/download/latest/linux_64
RUN tar xzf ./postman-agent.tar.gz