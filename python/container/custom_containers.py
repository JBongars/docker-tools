import subprocess
import os

from .utils import (
    get_dtools_image_name,
    gethomedir,
    gettempdir,
    attach_git,
    attach_work,
    set_hostname,
)


def availalbe_containers():
    return {
        "ubuntu": ubuntu,
        "dubuntu": dubuntu,
        "aws": aws,
        "github_actions": github_actions,
        "ngrok": ngrok,
        "yumdownloader": yumdownloader,
    }


def attach_terraform_token():
    return f"-v {gethomedir()}/.terraform.d:/root/.terraform.d"


def run_command(command, silent=False):
    if not silent:
        print("command = ", command)
    subprocess.run(
        command, shell=True, check=True, stdout=subprocess.DEVNULL if silent else None
    )


def ubuntu(args_string):
    run_command(
        f"docker run -ti {attach_work()}  {set_hostname('dtools-ubuntu')} {attach_git()} --rm {args_string} ubuntu:latest bash"
    )


def dubuntu(args_string):
    run_command(
        f"docker run -ti {attach_work()}  {set_hostname('dtools-dubuntu')} {attach_git()} --rm {args_string} dtools_ubuntu:latest zsh"
    )


def aws(args_string):
    run_command(
        f"docker run -it {attach_work()}  {set_hostname('dtools-aws')} {attach_git()} {attach_terraform_token()} -v {gethomedir()}/.aws:/root/.aws --rm {args_string} dtools_aws:latest zsh"
    )


def yumdownloader(args_string):
    print("Downloading RPMs...")
    run_command(
        f'docker run {attach_work()} --rm dtools_yumdownloader:latest bash -c "/tmp/.yumdownloader/download.sh /work/rpm.tar.gz {args_string}"'
    )

    print("Testing Installation...")
    run_command(
        f'docker run {attach_work()} --rm dtools_yumdownloader:latest bash -c "/tmp/.yumdownloader/install.sh /work/rpm.tar.gz"'
    )

    print("Success!")


def ngrok(args_string):
    run_command(f"docker run --network host --rm {args_string} dtools_ngrok:latest")


def github_actions(args_string):
    image_name = get_dtools_image_name("github_actions")
    command = f"docker run -ti --rm {args_string} {image_name}"
    run_command(command)
