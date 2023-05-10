import subprocess


def get_default_session_path():
    return "/usr/dtools/session"


def exec_into_container(container_id, command):
    subprocess.run(f"docker exec {container_id} {command}",
                   shell=True,
                   check=True)


def save_env_in_running_container(container_id, session_path):
    script_header = '''
    #!/bin/bash

    # This script saves the environment variables of a running container to a file.
    # Generated automatically by dtools
    # ------------
    '''
    command = f"mkdir {session_path} && cat <<EOF > {session_path}/env.sh {script_header} EOF && env | sed \"s/^/export /\" >> /usr/session/env.sh"

    exec_into_container(container_id, command)


def save_container_as_tar(container_id, tar_path):
    save_env_in_running_container(container_id, get_default_session_path())
    subprocess.run(f"docker export {container_id} -o {tar_path}",
                   shell=True,
                   check=True)


def run():
    pass