#!/bin/bash

repo_name=$(npm view "$(dirname "$(dirname "$(realpath "$0")")")" docker_repository)
images=$(docker images --filter "reference=${repo_name}/dtools_*" --format "{{.Repository}}:{{.Tag}}")

echo "$images" | parallel -j0 -I{} sh -c 'echo {} is pushing... && docker push {} > /dev/null && echo -en "\r{} done"'
