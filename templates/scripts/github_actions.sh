#!/bin/bash

set -e

script_dir=$(dirname $0)

handle_error() {
  echo "attempting to remove github actions configuration"
  "$script_dir/config.sh" remove --token $GITHUB_TOKEN
  exit 1
}
trap handle_error ERR

set +u
echo "configuring github actions on $GITHUB_REPO_URL"

"$script_dir/config.sh" --url $GITHUB_REPO_URL --token $GITHUB_TOKEN
"$script_dir/run.sh"