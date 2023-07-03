import subprocess

from .utils import get_dtools_image_name, gethomedir, attach_git, attach_work


def availalbe_containers():
    return {
        "ubuntu": ubuntu,
        "dubuntu": dubuntu,
        "aws": aws,
        "github_actions": github_actions,
        "ngrok": ngrok
    }


def attach_terraform_token():
    return f"-v {gethomedir()}/.terraform.d:/root/.terraform.d"


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


def aws(args_string):
    subprocess.run(
        f"docker run -it {attach_work()} {attach_git()} {attach_terraform_token()} -v {gethomedir()}/.aws:/root/.aws --rm {args_string} dtools_aws:latest zsh",
        shell=True,
        check=True)


def ngrok(args_string):
    subprocess.run(
        f"docker run --network host --rm {args_string} dtools_ngrok:latest",
        shell=True,
        check=True)


def github_actions(args_string):
    image_name = get_dtools_image_name("github_actions")
    subprocess.run(f"docker run -ti --rm {args_string} {image_name}",
                   shell=True,
                   check=True)
