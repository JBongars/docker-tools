import argparse
import os
import signal
import subprocess

from .utils import get_dtools_image_name, attach_git, attach_work, set_hostname


def availalbe_containers():
    return {
        "kube": kube,
        "awskube": awskube,
    }


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


def is_dood():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dood', action='store_true', help='enable dood mode')
    args, unknown = parser.parse_known_args()
    return args.dood, unknown


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


def kube(args_string):
    image_name = get_dtools_image_name("kube")
    dood_command = f"docker run -ti {attach_work()}  {set_hostname('dtools-kube-dood')} {attach_git()} --rm -v /var/run/docker.sock:/var/run/docker.sock {args_string} {image_name} zsh"
    dind_command = f"docker run -d {attach_work()}  {set_hostname('dtools-kube-dind')} {attach_git()} --privileged {args_string} {image_name}"
    run_docker_container(image_name, dood_command, dind_command)


def awskube(args_string):
    image_name = get_dtools_image_name("awskube")
    dood_command = f"docker run -it {attach_work()}  {set_hostname('dtools-awskube-dood')} {attach_git()} -v {os.path.expanduser('~')}/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock --rm {args_string} {image_name} zsh"
    dind_command = f"docker run -d {attach_work()}  {set_hostname('dtools-awskube-dind')} {attach_git()} -v {os.path.expanduser('~')}/.aws:/root/.aws --privileged {args_string} {image_name}"
    run_docker_container(image_name, dood_command, dind_command)
