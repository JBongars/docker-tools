FROM julien23/dtools_ubuntu:latest

# DNS Utilities
RUN apt-get -y install dnsutils

# Docker (need to mount docker socket DooD)
RUN apt-get install -y docker.io

# Docker dependencies
RUN apt-get install -y iptables e2fsprogs xfsprogs xz-utils pigz

# # Docker (need to mount docker socket DooD)
# RUN apt-get install -y docker.io

ENV DOCKER_CHANNEL=stable \
	DOCKER_VERSION=23.0.1 \
	DOCKER_COMPOSE_VERSION=v2.16.0 \
	BUILDX_VERSION=v0.10.3 \
	DEBUG=false

# Docker and buildx installation
# RUN set -eux; \
# 	\
# 	arch="$(uname -m)"; \
# 	case "$arch" in \
#         # amd64
# 		x86_64) dockerArch='x86_64' ; buildx_arch='linux-amd64' ;; \
#         # arm32v6
# 		armhf) dockerArch='armel' ; buildx_arch='linux-arm-v6' ;; \
#         # arm32v7
# 		armv7) dockerArch='armhf' ; buildx_arch='linux-arm-v7' ;; \
#         # arm64v8
# 		aarch64) dockerArch='aarch64' ; buildx_arch='linux-arm64' ;; \
# 		*) echo >&2 "error: unsupported architecture ($arch)"; exit 1 ;;\
# 	esac; \
# 	\
# 	if ! wget -O docker.tgz "https://download.docker.com/linux/static/${DOCKER_CHANNEL}/${dockerArch}/docker-${DOCKER_VERSION}.tgz"; then \
# 		echo >&2 "error: failed to download 'docker-${DOCKER_VERSION}' from '${DOCKER_CHANNEL}' for '${dockerArch}'"; \
# 		exit 1; \
# 	fi; \
# 	\
# 	tar --extract \
# 		--file docker.tgz \
# 		--strip-components 1 \
# 		--directory /usr/local/bin/ \
# 	; \
# 	rm docker.tgz; \
# 	if ! wget -O docker-buildx "https://github.com/docker/buildx/releases/download/${BUILDX_VERSION}/buildx-${BUILDX_VERSION}.${buildx_arch}"; then \
# 		echo >&2 "error: failed to download 'buildx-${BUILDX_VERSION}.${buildx_arch}'"; \
# 		exit 1; \
# 	fi; \
# 	mkdir -p /usr/local/lib/docker/cli-plugins; \
# 	chmod +x docker-buildx; \
# 	mv docker-buildx /usr/local/lib/docker/cli-plugins/docker-buildx; \
# 	\
# 	dockerd --version; \
# 	docker --version; \
# 	docker buildx version

COPY modprobe entrypoint.sh /usr/local/bin/
COPY supervisor/ /etc/supervisor/conf.d/
COPY logger.sh /opt/bash-utils/logger.sh
# COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/modprobe

# Docker compose installation
RUN curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
	&& chmod +x /usr/local/bin/docker-compose && docker-compose version

VOLUME /var/lib/docker

RUN apt-get install -y iputils-ping

# ENTRYPOINT ["entrypoint.sh"]
CMD ["zsh"]