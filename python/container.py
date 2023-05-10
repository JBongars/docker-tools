import requests
import utils
import glob
import hashlib
import os
import subprocess
import sys
import signal
import argparse


def getcwd():
    return f"\"{os.getcwd()}\""


def get_repository_no_cache():
    package_json_path = os.path.join(getcwd(), "package.json")
    if os.path.isfile(package_json_path):
        with open(package_json_path) as f:
            if not '"docker_repository": "' in f.read():
                return "julien23"
            return f.read().split('"docker_repository": "')[1].split('"')[0]
    return "julien23"


get_repository = utils.cache_no_args(get_repository_no_cache)


def get_dtools_image_name(base_name, version="latest"):
    print("base_name: ", base_name)
    if ":" in base_name:
        return f"{get_repository()}/dtools_{base_name}"

    return f"{get_repository()}/dtools_{base_name}:{version}"


def gethomedir():
    return f"\"{os.path.expanduser('~')}\""


def is_dood():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dood', action='store_true', help='enable dood mode')
    args, unknown = parser.parse_known_args()
    return args.dood, unknown


def attach_git():
    return f"-v {gethomedir()}/.gitconfig:/root/.gitconfig -v {gethomedir()}/.netrc:/root/.netrc -v {gethomedir()}/.ssh:/root/.ssh -v {gethomedir()}/.git-credentials:/root/.git-credentials"


def attach_work():
    return f"-v {getcwd()}:/work"


def get_display_env():
    if os.name == 'nt':
        powershell_command = "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'vEthernet (WSL)').IPAddress"
        wsl_port = subprocess.run(
            f'powershell -Command "{powershell_command}"',
            capture_output=True,
            text=True).stdout.rstrip('\n') + ":0"
        return wsl_port
    else:
        print('could not set port... not implemented')


def graphical_application(container, args_string):
    display_ip = get_display_env()
    subprocess.run(
        f"docker run -ti --rm -e DISPLAY={display_ip} {args_string} {container}",
        shell=True,
        check=True)


def stop_container(container_id):
    print("Stopping container...")
    subprocess.run(f"docker stop {container_id}", shell=True, check=True)

    print("Removing container...")
    subprocess.run(f"docker rm {container_id}", shell=True, check=True)


def safely_exec_container(container_id, exec_string):
    cleanup_flag = True

    def cleanup_handler(_signum, _frame):
        if cleanup_flag:
            stop_container(container_id)

    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGABRT):
        signal.signal(sig, cleanup_handler)

    subprocess.run(f"docker exec -it {container_id} {exec_string}",
                   shell=True,
                   check=True)
    stop_container(container_id)

    cleanup_flag = False


def run_docker_container(image_name,
                         run_dood_string,
                         run_dind_string,
                         exec_dind_string="zsh"):

    if is_dood():
        # ugly patch to remove the --dood flag
        if "--dood " in run_dood_string:
            run_dood_string = run_dood_string.replace("--dood", "")
        subprocess.run(run_dood_string, shell=True, check=True)
        return

    subprocess.run(run_dind_string, shell=True, check=True)
    container_id = subprocess.check_output(
        f"docker ps -q -f ancestor={image_name}",
        shell=True).decode().strip().split("\n")[0]

    safely_exec_container(container_id, exec_dind_string)


def get_local_dockerfile(path="."):
    files = []

    if os.path.isdir(path):
        files = glob.glob(f"{path}/Dockerfile*")
    else:
        files = glob.glob(f"{path}")

    if not files:
        return None

    if len(files) == 1:
        return files[0]

    print(f'Multiple Dockerfiles found...')
    for file in files:
        print(f'- {file}')

    # prefer Dockerfile.dev* over Dockerfile
    for file in files:
        if "Dockerfile.dev" in file:
            return file

    return files[0]


def run_local_container(path, args_string):
    dockerfile = get_local_dockerfile(path)

    if not dockerfile:
        print("No Dockerfile located in the current directory")
        sys.exit(1)

    print(f"Using Dockerfile {dockerfile}...")

    cwd = getcwd()
    id = hashlib.sha256(cwd.encode()).hexdigest()
    image_name = f"dlocal-{id}"

    print(f"Building image {image_name}...")
    subprocess.run(
        f"docker build {path} -f {dockerfile} -t {image_name}:latest")

    subprocess.run(
        f"docker run -it -v {getcwd()}:/work --rm {args_string} {image_name}")

    print('Cleaning up...')
    subprocess.run(f"docker rmi {image_name}")

    sys.exit(0)


def ubuntu(args_string):
    subprocess.run(
        f"docker run -ti {attach_work()} {attach_git()} --rm {args_string} ubuntu:latest bash",
        shell=True,
        check=True)


def dubuntu(args_string):
    subprocess.run(
        f"docker run -ti {attach_work()} {attach_git()} --rm {args_string} dtools_ubuntu:latest zsh",
        shell=True,
        check=True)


def kube(args_string):
    image_name = get_dtools_image_name("kube")
    dood_command = f"docker run -ti {attach_work()} {attach_git()} --rm -v /var/run/docker.sock:/var/run/docker.sock {args_string} {image_name} zsh"
    dind_command = f"docker run -d {attach_work()} {attach_git()} --privileged {args_string} {image_name}"
    run_docker_container(image_name, dood_command, dind_command)


def aws(args_string):
    subprocess.run(
        f"docker run -it {attach_work()} {attach_git()} -v {gethomedir()}/.aws:/root/.aws --rm {args_string} julien23/dtools_aws:latest zsh",
        shell=True,
        check=True)


def awskube(args_string):
    image_name = get_dtools_image_name("awskube")
    dood_command = f"docker run -it {attach_work()} {attach_git()} -v {os.path.expanduser('~')}/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock --rm {args_string} {image_name} zsh"
    dind_command = f"docker run -d {attach_work()} {attach_git()} -v {os.path.expanduser('~')}/.aws:/root/.aws --privileged {args_string} {image_name}"
    run_docker_container(image_name, dood_command, dind_command)


# TODO - add volume mounting for insomnia configuration
def insomnia(args_string):
    image_name = get_dtools_image_name("insomnia")
    graphical_application(image_name, f"--cap-add SYS_ADMIN {args_string}")


def firefox(args_string):
    image_name = get_dtools_image_name("firefox")
    graphical_application(image_name, args_string)


def github_actions(args_string):
    image_name = get_dtools_image_name("github_actions")
    subprocess.run(f"docker run -ti --rm {args_string} {image_name}",
                   shell=True,
                   check=True)


def check_if_docker_image_exists_local(image_name, version="latest"):
    try:
        if not ":" in image_name:
            image_name = f"{image_name}:{version}"

        subprocess.run(
            f"docker inspect {image_name}",
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        return True
    except:
        return False


def check_if_docker_image_exists_remote(image_name, version="latest"):
    if ":" in image_name:
        image_name, version = image_name.split(":")

    url = f"https://hub.docker.com/v2/repositories/{image_name}/tags/{version}"
    response = requests.get(url)
    return response.status_code == 200


def check_if_docker_image_exists(image_name, version="latest"):
    if check_if_docker_image_exists_local(image_name):
        return True

    return check_if_docker_image_exists_remote(image_name, version)


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


def import_state_to_base_image(image_name, state_file_path):
    print("Importing state...")
    new_image = ""
    subprocess.run(
        f"docker import {state_file_path} {image_name}",
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
    )

    return image_name


def run_container_with_state(function_name, state_file_path, args_string):
    image_name, start_script = get_image_and_start_script_from_function_name(
        function_name)

    state_parent_dir = os.path.dirname(state_file_path)
    if not os.path.isdir(state_parent_dir):
        os.makedirs(state_parent_dir)

    if os.path.isfile(state_file_path):
        image_name = import_state_to_base_image(image_name, state_file_path)

    command = f"docker create -ti {attach_work()} {attach_git()} {args_string} {image_name} {start_script}"

    container_id = subprocess.run(
        command,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8").strip()

    subprocess.run(f"docker start -ai {container_id}", shell=True, check=True)
    subprocess.run(f"docker export {container_id} > {state_file_path}",
                   shell=True,
                   check=True)
    subprocess.run(f"docker rm {container_id}", shell=True, check=True)


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
    args_string = " ".join(args[1:])

    if function_name in globals():
        return globals()[function_name](args_string)

    if function_name[0] == "." or function_name[0] == "/":
        return run_local_container(function_name, args_string)

    print(f"Function '{function_name}' not found. Using default...")
    try:
        for arg in args_string.split(" "):
            if arg == "--persist":
                print("not implemented yet...")
                sys.exit(1)
                args_string_without_preserve = args_string.replace(arg, "")
                return run_container_with_state(function_name,
                                                get_default_state_file_path(),
                                                args_string_without_preserve)

        return run_container(function_name, args_string)
    except:
        print(f"Function '{function_name}' could not be run.")
        sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]
    run(args)