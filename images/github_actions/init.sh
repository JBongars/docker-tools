#!/bin/bash

set -e
set -u

script_dir=$(dirname $0)
environment_file="~/.github_actions"

if [ -f "$environment_file" ]; then
  echo "loading environment variables from $environment_file"
  . $environment_file
fi

pat_token=${GITHUB_PAT_TOKEN:-}
# looks something like this: https://github.com/owner/my-repo
repo_url=${GITHUB_REPO_URL:-}
runner_name=${GITHUB_RUNNER_NAME:-"$(hostname)"}
export self_hosted_token=${GITHUB_TOKEN:-}
owner=$(echo $repo_url | cut -d'/' -f4)
repo=$(echo $repo_url | cut -d'/' -f5)
is_configured=${GITHUB_IS_CONFIGURED:-}

if [ -z "$self_hosted_token"]; then
  echo "No self_hosted_token found! generating self hosted token.."
  echo $pat_token | gh auth login --with-token 
  self_hosted_token=$(gh api -X POST repos/$owner/$repo/actions/runners/registration-token | jq -r .token)
fi

# In case of ctrl+c, remove github actions configuration
handle_error() {
  echo "attempting to remove github actions configuration"
  "$script_dir/config.sh" remove --token "$self_hosted_token"
  echo -n "" > "$environment_file" # clear environment file
  exit 1
}
trap 'handle_error' EXIt SIGINT SIGTERM

set +e # ignore errors as can be false negative

if [ "$is_configured" != "0" ]; then
  echo "configuring github actions on $GITHUB_REPO_URL"

  "$script_dir/config.sh" --url $repo_url --token $self_hosted_token --name $runner_name --unattended
  is_configured=$?
fi

echo -n "
GITHUB_PAT_TOKEN=$pat_token
GITHUB_REPO_URL=$repo_url
GITHUB_TOKEN=$self_hosted_token
GITHUB_RUNNER_NAME=$runner_name
GITHUB_IS_CONFIGURED=$is_configured
" > $environment_file

echo "running github actions on $GITHUB_REPO_URL"
"$script_dir/run.sh" --unattended