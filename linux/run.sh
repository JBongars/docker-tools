#!/bin/bash

# Check if the shell is zsh; if not, switch to zsh and re-run this script
if [[ "$(ps -p $$ -ocomm=)" != "zsh" ]]; then
  exec zsh "$0"
fi

ubuntu() {
  docker run -ti -v "${PWD}:/work" "$@" ubuntu bash
}

dubuntu() {
  docker run -ti -v "${PWD}:/work" "$@" julien23/dtools_ubuntu:latest zsh
}

kube() {
  docker run -ti -v "${PWD}:/work" -v "/var/run/docker.sock:/var/run/docker.sock" "$@" julien23/dtools_kube:latest zsh
}

aws() {
  docker run -it -v "${PWD}:/work" -v "$HOME/.aws:/root/.aws" "$@" julien23/dtools_aws:latest zsh
}

awskube() {
  docker run -it -v "${PWD}:/work" -v "$HOME/.aws:/root/.aws" -v "/var/run/docker.sock:/var/run/docker.sock" "$@" julien23/dtools_awskube:latest zsh
}

if [ "$#" -eq 0 ]; then
    echo "Please specify a function to call as an argument."
else
    functionName=$1

    if type "$functionName" &> /dev/null; then
        remainingArgs=("${@:2}")
        "$functionName" "${remainingArgs[@]}"
    else
        echo "Function '$functionName' not found."
    fi
fi
