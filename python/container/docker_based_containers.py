import argparse
import os
import signal
import subprocess

from .utils import get_dtools_image_name, attach_git, attach_work, set_hostname

DEFAULT_EXEC_STRING = "/bin/sh"
DOOD_FLAG = "--dood"
DIND_FLAG = "--dind"


def availalbe_containers():
    return {"kube": kube, "awskube": awskube, "ddocker": ddocker}


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

    subprocess.run(
        f"docker exec -it {container_id} {exec_string}", shell=True, check=True
    )
    stop_container(container_id)

    cleanup_flag = False


def run_dood_container(
    image_name,
    base_command,
    args_string,
    hostname=None,
    exec_string=DEFAULT_EXEC_STRING,
):
    if hostname is None:
        hostname = f"dtools-{image_name}-dood"
    cmd = f"{base_command} -v /var/run/docker.sock:/var/run/docker.sock {set_hostname(hostname)} {args_string} {image_name} {exec_string}"

    print("Running command: ", cmd)
    return subprocess.run(cmd, shell=True, check=True)


def run_dind_container(
    image_name,
    base_command,
    args_string,
    hostname=None,
    exec_dind_string=DEFAULT_EXEC_STRING,
):
    if hostname is None:
        hostname = f"dtools-{image_name}-dind"

    # privileged is required for docker in docker
    # docs: https://hub.docker.com/_/docker > Rootless
    cmd = f"{base_command} -d --privileged {set_hostname(hostname)} {args_string} {image_name}"

    print("Running command: ", cmd)
    subprocess.run(cmd, shell=True, check=True)
    container_id = (
        subprocess.check_output(f"docker ps -q -f ancestor={image_name}", shell=True)
        .decode()
        .strip()
        .split("\n")[0]
    )
    safely_exec_container(container_id, exec_dind_string)


def run_docker_container(
    image_name, dood_command, dind_command, args_string, exec_dind_string="fish"
):
    print(args_string)
    if DOOD_FLAG in args_string:
        print("Running with dood flag...")
        args_string = args_string.replace(DOOD_FLAG, "")
        return run_dood_container(image_name, dood_command, args_string)

    else:
        print("Running with dind flag...")
        if DIND_FLAG in args_string:
            args_string = args_string.replace(DIND_FLAG, "")
        return run_dind_container(
            image_name, dind_command, args_string, exec_dind_string
        )


def ddocker(args_string):
    image_name = get_dtools_image_name("docker")
    dood_command = f"docker run -ti {attach_work()} {attach_git()} --rm"
    dind_command = f"docker run {attach_work()} {attach_git()}"
    run_docker_container(
        image_name, dood_command, dind_command, args_string, exec_dind_string="fish"
    )


def kube(args_string):
    image_name = get_dtools_image_name("kube")
    dood_command = f"docker run -ti {attach_work()} {attach_git()} --rm"
    dind_command = f"docker run {attach_work()} {attach_git()}"
    run_docker_container(
        image_name, dood_command, dind_command, args_string, exec_dind_string="fish"
    )


def awskube(args_string):
    image_name = get_dtools_image_name("awskube")
    dood_command = f"docker run -it {attach_work()} {attach_git()} -v {os.path.expanduser('~')}/.aws:/root/.aws --rm"
    dind_command = f"docker run {attach_work()} {attach_git()} -v {os.path.expanduser('~')}/.aws:/root/.aws"
    run_docker_container(
        image_name, dood_command, dind_command, args_string, exec_dind_string="fish"
    )
