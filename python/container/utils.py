import os
import subprocess
from re import sub as re_sub

import requests

FLAG_TEMPLATE = "-dtools-"


def get_flags(args):
    flags = []
    for arg in args.split(" "):
        if FLAG_TEMPLATE in arg:
            flags.append(arg.replace(FLAG_TEMPLATE, "-"))
    return flags


def prune_flags(args):
    flags = get_flags(args)
    for flag in flags:
        args = args.replace(f"{FLAG_TEMPLATE}{flag}", "")
    return flags, args


def cache_no_args(f: callable) -> callable:
    result = ""

    def wrapper():
        nonlocal result
        if result == "":
            result = f()
        return result

    return wrapper


def getcwd():
    return f'"{os.getcwd()}"'


def get_repository_no_cache():
    package_json_path = os.path.join(getcwd(), "package.json")
    if os.path.isfile(package_json_path):
        with open(package_json_path) as f:
            if not '"docker_repository": "' in f.read():
                return "julien23"
            return f.read().split('"docker_repository": "')[1].split('"')[0]
    return "julien23"


get_repository = cache_no_args(get_repository_no_cache)


def get_dtools_image_name(base_name, version="latest"):
    if ":" in base_name:
        return f"{get_repository()}/dtools_{base_name}"

    return f"{get_repository()}/dtools_{base_name}:{version}"


def gethomedir():
    return f"\"{os.path.expanduser('~')}\""


def gettempdir():
    if os.path.exists(os.environ["TEMP"]):
        return os.environ["TEMP"]
    if os.path.exists("/usr/tmp"):
        return "/usr/tmp"
    if os.path.exists("/tmp"):
        return "/tmp"
    return None


def attach_git():
    return f"-v {gethomedir()}/.gitconfig:/root/.gitconfig -v {gethomedir()}/.netrc:/root/.netrc -v {gethomedir()}/.ssh:/root/.ssh -v {gethomedir()}/.git-credentials:/root/.git-credentials"


def attach_work():
    return f"-v {getcwd()}:/work"


def set_hostname(name):
    sanitized_name = re_sub(r"[^a-z0-9\-]+", "-", name.lower())
    return f"--hostname {sanitized_name}"


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
