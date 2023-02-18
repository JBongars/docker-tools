#!/bin/bash

# Check if the shell is zsh; if not, switch to zsh and re-run this script
if [[ "$(ps -p $$ -ocomm=)" != "zsh" ]]; then
  exec zsh "$0"
fi

# Get the directory containing the script file
script_dir="$(dirname "$(readlink -f "$0")")"

# Define the text to add to the shell configuration file
dockerToolsText=$(cat <<EOF
# ----------
# DOCKER TOOLS
alias de="${script_dir}/run.sh"
# ----------
EOF
)

# Get the current shell configuration file name
if [ -f "${HOME}/.zshrc" ]; then
    config_file="${HOME}/.zshrc"
elif [ -f "${HOME}/.bashrc" ]; then
    config_file="${HOME}/.bashrc"
else
    echo "No shell configuration file found."
    exit 1
fi

# Check if the shell configuration file already contains the Docker tools text
if grep -qF "${dockerToolsText}" "${config_file}"; then
    echo "Docker tools is already installed."
else
    # Append the Docker tools text to the shell configuration file
    echo "${dockerToolsText}" >> "${config_file}"
    source ${config_file}
    echo "Docker tools has been installed."
fi