# Generated Manually
# TODO: Feature copy root folder for *.dockerfile.j2 directory 

FROM rockylinux:8.9

RUN yum install -y epel-release

# RHEL Base
RUN yum update -y  yum upgrade -y

RUN yum install -y \
    curl \
    bash \
    findutils \
    createrepo \
    dos2unix \
;

RUN yum install findutils -y

RUN mkdir -p /tmp/.yumdownloader
COPY ./.yumdownloader /tmp/.yumdownloader/
RUN dos2unix /tmp/.yumdownloader/*
RUN chmod +x /tmp/.yumdownloader/*

CMD ["/bin/bash"]

WORKDIR /work    
