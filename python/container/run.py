import requests
import os
import subprocess
import sys
import signal

from .catalogue import get_available_containers
from .utils import attach_git, attach_work, check_if_docker_image_exists, get_dtools_image_name, prune_flags
from .local_containers import run_local_container
from .temp_container import run_temp_container


def get_image_and_start_script_from_function_name(function_name):
    image_name = get_dtools_image_name(function_name)
    start_script = "zsh"

    if not check_if_docker_image_exists(image_name):
        if not check_if_docker_image_exists(function_name):
            print(f"Image {image_name} does not exist")
            sys.exit(1)

        # override default cmd to open shell
        start_script = "/bin/sh"
        image_name = function_name

    print(f"Using image {image_name}...")
    return image_name, start_script


def get_default_state_file_path():
    return os.path.join(".", ".dtools", "state.tar")


# def import_state_to_base_image(image_name, state_file_path):
#     print("Importing state...")
#     new_image = ""
#     subprocess.run(
#         f"docker import {state_file_path} {image_name}",
#         shell=True,
#         check=True,
#         stdout=subprocess.PIPE,
#     )

#     return image_name

# def run_container_with_state(function_name, state_file_path, args_string):
#     image_name, start_script = get_image_and_start_script_from_function_name(
#         function_name)

#     state_parent_dir = os.path.dirname(state_file_path)
#     if not os.path.isdir(state_parent_dir):
#         os.makedirs(state_parent_dir)

#     if os.path.isfile(state_file_path):
#         image_name = import_state_to_base_image(image_name, state_file_path)

#     command = f"docker create -ti {attach_work()} {attach_git()} {args_string} {image_name} {start_script}"

#     container_id = subprocess.run(
#         command,
#         shell=True,
#         check=True,
#         stdout=subprocess.PIPE,
#     ).stdout.decode("utf-8").strip()

#     subprocess.run(f"docker start -ai {container_id}", shell=True, check=True)
#     subprocess.run(f"docker export {container_id} > {state_file_path}",
#                    shell=True,
#                    check=True)
#     subprocess.run(f"docker rm {container_id}", shell=True, check=True)


def run_container(function_name, args_string):
    image_name, start_script = get_image_and_start_script_from_function_name(
        function_name)

    command = f"docker run -ti {attach_work()} {attach_git()} --rm {args_string} {image_name} {start_script}"
    print("command = ", command)
    return subprocess.run(command, shell=True, check=True)


def run(args):
    if len(args) < 1:
        print("Please specify a function to call as an argument.")
        return

    function_name = args[0]
    flags, args_string = prune_flags(" ".join(args[1:]))

    if function_name in get_available_containers().keys():
        return get_available_containers()[function_name](args_string)

    if function_name[0] == "." or function_name[0] == "/":
        return run_local_container(function_name, args_string)

    print(f"Function '{function_name}' not found. Using default...")
    try:
        return run_container(function_name, args_string)
    except:
        print(f"Function '{function_name}' could not be run.")
        sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]
    run(args)