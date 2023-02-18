
function push_container_to_docker_hub($container_name) {
  $docker_hub_username = "julien23"
  $docker_hub_repository = $docker_hub_username + "/" + $container_name
  $tagged_image = $docker_hub_repository + ":latest"

#   docker login --username=$docker_hub_username
  docker tag $container_name $tagged_image
  docker push $tagged_image
}

# ubuntu
docker build -f ${PSScriptRoot}\..\images\Dockerfile.ubuntu -t dtools_ubuntu:latest ${PSScriptRoot}\..\.containers

# docker
docker build -f ${PSScriptRoot}\..\images\Dockerfile.ubuntu -t dtools_docker:latest ${PSScriptRoot}\..\.containers

# kube
docker build -f ${PSScriptRoot}\..\images\Dockerfile.kube -t dtools_kube:latest ${PSScriptRoot}\..\.containers

# push all containers to docker hub
push_container_to_docker_hub "dtools_ubuntu"
push_container_to_docker_hub "dtools_docker"
push_container_to_docker_hub "dtools_kube"