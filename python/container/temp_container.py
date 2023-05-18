from distutils.dir_util import copy_tree
import hashlib
import os
import shutil
import subprocess

from .utils import attach_git, attach_work, getcwd


def get_templates_path():
    current_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(current_path, "../../templates"))


def get_template_base_path(image_os):
    script_path = get_templates_path()
    base_path = os.path.join(script_path, f"modules/{image_os}/base.j2")

    print("base_path= ", base_path)

    return base_path if os.path.exists(base_path) else None


def extract_os_from_args(args_string):
    if "--os-" in args_string:
        return args_string.split("--os-")[1].split(
            " ")[0], args_string.replace(f"--os-{os}", "")
    return None, args_string


def get_base(image_os):
    if image_os is None:
        return None

    base_path = get_template_base_path(image_os)
    if base_path is None:
        return None

    with open(base_path) as f:
        return f.read()


def get_temp_folder_path():
    if os.path.exists(os.environ["TEMP"]):
        return os.environ["TEMP"]
    if os.path.exists("/usr/tmp"):
        return "/usr/tmp"
    if os.path.exists("/tmp"):
        return "/tmp"
    return None


def create_temp_dockerfile(image, image_version, base):
    temp_folder_path = get_temp_folder_path()
    if temp_folder_path is None:
        print("Could not find a temp folder. Creating...")
        os.mkdir(os.path.join(getcwd(), ".dtemp"))
        temp_folder_path = os.path.join(getcwd(), ".dtemp")

    docker_folder_path = os.path.join(temp_folder_path, f"dtemp-{image}")
    if not os.path.exists(docker_folder_path):
        os.mkdir(docker_folder_path)

    dockerfile_path = os.path.join(docker_folder_path, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(f"FROM {image}:{image_version}\n")
        f.write(base)
        f.write("\n")
        f.write("CMD [\"/bin/bash\"]")

    copy_tree(f"{get_templates_path()}/scripts/",
              f"{docker_folder_path}/scripts/")

    return docker_folder_path


def build_temp_image(image_name, image_version, dockerfile_path):
    tag = f"dtemp-{image_name}:{image_version}"
    command = f"docker build {dockerfile_path} -t {tag}"
    print(f"Build command: {command}")

    subprocess.run(command, shell=True)
    return tag


def get_image_name_version(image):
    if len(image.split(":")) < 2:
        return image, "latest"
    return image.split(":")[0], image.split(":")[1]


def run_temp_container(image, args_string):
    image_os, args_string = extract_os_from_args(args_string)
    image_name, image_version = get_image_name_version(image)

    print(f"Running container <{image_name}:{image_version}>")

    if image_os is None:
        image_os = image_name

    base = get_base(image_os)

    if base is None:
        print(f"Base template for {image_os} not found.")
        return

    dockerfile_path = create_temp_dockerfile(image_name, image_version, base)
    print(f"Using Dockerfile {dockerfile_path}...")

    tag = build_temp_image(image_name, image_version, dockerfile_path)
    print(f"Built image {tag}...")

    command = f"docker run -it {attach_git()} {attach_work()} --rm {args_string} {tag}"
    print(command)

    try:
        subprocess.run(command, shell=True)
    except:
        print(f"Container '{image_name}' exited or could not be run.")

    print('Cleaning up...')
    # shutil.rmtree(os.path.dirname(dockerfile_path))