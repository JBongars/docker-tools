
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/insomnia.dockerfile.j2
# AND RUN python ^/python/build.py
# ------------

FROM ubuntu:22.04

ARG VERSION=2023.1.0

RUN apt-get -y update && apt-get -y upgrade

RUN apt-get -y install apt-transport-https curl libgbm1 libasound2

WORKDIR /insomnia

RUN curl -L https://github.com/Kong/insomnia/releases/download/core%40${VERSION}/Insomnia.Core-${VERSION}.deb -o insomnia.deb

# WARNING, this takes a veeery long time
RUN apt-get -y install ./insomnia.deb

RUN adduser insomnia

USER insomnia

CMD ["insomnia"]