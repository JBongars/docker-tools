import subprocess
import sys

from . import catalogue, utils, local_containers, temp_container


def get_image_and_start_script_from_function_name(function_name):
    image_name = utils.get_dtools_image_name(function_name)
    start_script = "zsh"

    if not utils.check_if_docker_image_exists(image_name):
        if not utils.check_if_docker_image_exists(function_name):
            print(f"Image {image_name} does not exist")
            sys.exit(1)

        # override default cmd to open shell
        start_script = "/bin/sh"
        image_name = function_name

    print(f"Using image {image_name}...")
    return image_name, start_script


def run_container(function_name, args_string):
    image_name, start_script = get_image_and_start_script_from_function_name(
        function_name)

    command = f"docker run -ti {utils.attach_work()} {utils.attach_git()} --rm {args_string} {image_name} {start_script}"
    print("command = ", command)
    return subprocess.run(command, shell=True, check=True)


def run(args):
    if len(args) < 1:
        print("Please specify a function to call as an argument.")
        return

    function_name = args[0]
    flags, args_string = utils.prune_flags(" ".join(args[1:]))

    if function_name in catalogue.get_available_containers().keys():
        return catalogue.get_available_containers()[function_name](args_string)

    if function_name[0] == "." or function_name[0] == "/":
        return local_containers.run_local_container(function_name, args_string)

    if "_" == function_name[0]:
        return temp_container.run_temp_container(
            function_name.replace("_", ""), args_string)

    print(f"Function '{function_name}' not found. Using default...")
    try:
        return run_container(function_name, args_string)
    except:
        print(f"Function '{function_name}' could not be run.")
        sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]
    run(args)