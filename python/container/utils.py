import os


def cache_no_args(f: callable) -> callable:
    result = ""

    def wrapper():
        nonlocal result
        if result == "":
            result = f()
        return result

    return wrapper


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


get_repository = cache_no_args(get_repository_no_cache)


def get_dtools_image_name(base_name, version="latest"):
    if ":" in base_name:
        return f"{get_repository()}/dtools_{base_name}"

    return f"{get_repository()}/dtools_{base_name}:{version}"


def gethomedir():
    return f"\"{os.path.expanduser('~')}\""
