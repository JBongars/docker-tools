from distutils.dir_util import copy_tree
import hashlib
import os
import shutil
import subprocess
import time

from .utils import attach_git, attach_work, getcwd, set_hostname, gettempdir


def get_templates_path():
    current_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(current_path, "../../templates"))


def get_template_base_path(image_os):
    script_path = get_templates_path()
    base_path = os.path.join(script_path, f"modules/{image_os}/base.j2")

    return base_path if os.path.exists(base_path) else None


def get_template_footer_path(image_os):
    script_path = get_templates_path()
    base_path = os.path.join(script_path, f"modules/{image_os}/footer.j2")

    return base_path if os.path.exists(base_path) else None


def extract_no_cache_from_args(args_string):
    if "--no-cache" in args_string:
        return True, args_string.replace("--no-cache", "").strip()
    return False, args_string


def extract_os_from_args(args_string):
    if "--os-" in args_string:
        image_os = args_string.split("--os-")[1].split(" ")[0]
        return image_os, args_string.replace(f"--os-{image_os}", "").strip()
    return None, args_string


def get_base(image_os):
    if image_os is None:
        return None

    base_path = get_template_base_path(image_os)
    if base_path is None:
        return None

    footer = get_template_footer_path(image_os)

    with open(base_path) as f:
        base_content = f.read()

    if footer is not None:
        with open(footer) as f:
            base_content += f.read()

    return base_content


def create_temp_dockerfile(image, image_version, base):
    temp_folder_path = gettempdir()
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
        f.write('CMD ["/bin/fish"]')

    copy_tree(f"{get_templates_path()}/scripts/", f"{docker_folder_path}/scripts/")

    return docker_folder_path


def build_temp_image(image_name, image_version, build_args, dockerfile_path):
    tag = f"dtemp-{image_name}:{image_version}"
    command = f"docker build {dockerfile_path} -t {tag} {' '.join(build_args)}"
    print(f"Build command: {command}")

    subprocess.run(command, shell=True)
    return tag


def get_image_name_version(image):
    if len(image.split(":")) < 2:
        return image, "latest"
    return image.split(":")[0], image.split(":")[1]


def clean_up_dockerfile(dockerfile_path, tag):
    command = f"docker rmi {tag}"
    subprocess.run(command, shell=True)

    for i in range(5):
        try:
            shutil.rmtree(dockerfile_path)
            break
        except:
            time.sleep(1)


def run_temp_container(image, args_string):
    image_os, args_string = extract_os_from_args(args_string)
    image_name, image_version = get_image_name_version(image)
    no_cache, args_string = extract_no_cache_from_args(args_string)

    if image_os is None:
        image_os = image_name

    base = get_base(image_os)

    if base is None:
        print(f"Base template for {image_os} not found.")
        return

    hostname = f"t_{image}:{image_version}"
    build_args = []
    if no_cache:
        build_args.append("--no-cache")

    dockerfile_path = create_temp_dockerfile(image_name, image_version, base)
    tag = build_temp_image(image_name, image_version, build_args, dockerfile_path)
    command = f"docker run -it {attach_git()} {attach_work()}  {set_hostname(hostname)} --rm {args_string} {tag}"
    print(command)

    try:
        subprocess.run(command, shell=True)
    except:
        print(f"Container '{image_name}' exited or could not be run.")

    print("Cleaning up...")
    clean_up_dockerfile(dockerfile_path, tag)
