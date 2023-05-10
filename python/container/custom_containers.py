import os
import subprocess

from .utils import get_dtools_image_name
from .docker_based_containers import run_docker_container
from .run import attach_git, attach_work


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


def github_actions(args_string):
    image_name = get_dtools_image_name("github_actions")
    subprocess.run(f"docker run -ti --rm {args_string} {image_name}",
                   shell=True,
                   check=True)
