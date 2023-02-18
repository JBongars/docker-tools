#! /bin/bash

# Check if the shell is zsh; if not, switch to zsh and re-run this script
if [[ "$(ps -p $$ -ocomm=)" != "zsh" ]]; then
  exec zsh "$0"
fi

build-and-tag-image() {
  local imageName=$1
  local version=$2

  dockerfilePath="${scriptPath}/images/Dockerfile.${imageName}"
  localTagName="dtools_${imageName}:latest"
  tagName="julien23/dtools_${imageName}:${version}"
  latestTagName="julien23/dtools_${imageName}:latest"
  noCacheFlag=""
  if [ "$noCache" = true ]; then
    noCacheFlag="--no-cache"
  fi

  eval "docker build -f ${dockerfilePath} -t ${localTagName} ${noCacheFlag} .."
  docker tag "${localTagName}" "${tagName}"
  docker tag "${localTagName}" "${latestTagName}"
}

noCache=false
if [[ "$*" == *"--no-cache"* ]]; then
  noCache=true
fi

scriptPath=$(dirname "$(dirname "$(realpath "$0")")")
packageJsonPath="${scriptPath}/package.json"

version=$(jq -r '.version' "${packageJsonPath}")
repo_name=$(jq -r '.docker_repository' "${packageJsonPath}")

# Call the function for each Docker image to build and tag
build-and-tag-image "ubuntu" "${version}" "${repo_name}"
build-and-tag-image "docker" "${version}" "${repo_name}"
build-and-tag-image "kube" "${version}" "${repo_name}"
build-and-tag-image "aws" "${version}" "${repo_name}"
build-and-tag-image "awskube" "${version}" "${repo_name}"