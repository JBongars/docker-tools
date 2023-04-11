import os
import glob
import subprocess
import json
import sys
import jinja2
import re
import shutil


def get_template_header(image_name="<template>"):
    return f'''
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/{image_name}.dockerfile.j2
# AND RUN python ^/python/build.py {image_name}
# ------------

'''


def get_package_json():
    script_path = os.path.dirname(os.path.realpath(__file__))
    package_json_path = os.path.join(script_path, "..", "package.json")

    with open(package_json_path) as f:
        return json.load(f)


def get_project_version_no():
    return get_package_json()["version"]


def get_project_path():
    script_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(script_path, ".."))


def get_template_path():
    script_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(script_path, '..', f"templates")
    return os.path.abspath(template_path)


def get_repo_name():
    return get_package_json()["docker_repository"]


def get_jinja2_env():
    jinja_path = get_template_path()
    return jinja2.Environment(loader=jinja2.FileSystemLoader(jinja_path))


def substitute_copy_paths(template, dockerfile_path):
    template_path = get_template_path()
    print("template_path= ", template_path)

    # find all COPY statements
    pattern = r"COPY\s+((?:\S+/)*\S+)\s+(\S+)"
    matches = re.findall(pattern, template)

    # copy files and replace COPY statements
    for src, dest in matches:
        print(f"copying {src} to {dest}...")

        src_path = os.path.join(template_path, src)
        dest_path = os.path.join(dockerfile_path, os.path.basename(dest))
        print(f"src_path= {src_path} dest_path= {dest_path}")

        shutil.copy(src_path, dest_path)
        template = template.replace(f"COPY {src} {dest}",
                                    f"COPY ./{os.path.basename(dest)} {dest}")
    return template


def generate_docker_image(dockerfile_path, image_name):
    env = get_jinja2_env()
    template = env.get_template(f"{image_name}.dockerfile.j2")
    rendered_template = get_template_header(image_name) + template.render()

    if not os.path.exists(dockerfile_path):
        os.makedirs(dockerfile_path)

    rendered_template = substitute_copy_paths(rendered_template,
                                              dockerfile_path)

    with open(f"{dockerfile_path}/Dockerfile", "w") as f:
        f.write(rendered_template)


def build_docker_image(dockerfile_path, local_tag_name, build_args):
    subprocess.run(
        f"docker build -t {local_tag_name} {build_args} {dockerfile_path}",
        shell=True,
        check=True)


def tag_docker_image(current_tag, next_tag):
    subprocess.run(f"docker tag {current_tag} {next_tag}",
                   shell=True,
                   check=True)


def process_docker_image(image_name, version, repo_name, build_args):
    print("build_args= ", build_args)
    # weird quirk where docker needs the relative path not the abs path to build containers
    dockerfile_path = os.path.join(get_project_path(), "images", image_name)

    if not os.path.exists(dockerfile_path):
        os.makedirs(dockerfile_path)
        print(f"Directory {dockerfile_path} created")

    local_tag_name = f"dtools_{image_name}:latest"
    tag_name = f"{repo_name}/dtools_{image_name}:{version}"
    latest_tag_name = f"{repo_name}/dtools_{image_name}:latest"

    generate_docker_image(dockerfile_path, image_name)
    build_docker_image(dockerfile_path, local_tag_name, build_args)
    tag_docker_image(local_tag_name, tag_name)
    tag_docker_image(local_tag_name, latest_tag_name)


def build_all_images(build_args):
    repo_name = get_repo_name()
    version = get_project_version_no()
    extension = ".dockerfile.j2"

    image_paths = glob.glob(
        os.path.join(get_project_path(), f"templates/*{extension}"))
    images = [
        os.path.basename(elem).replace(extension, "") for elem in image_paths
    ]

    for image in images:
        process_docker_image(image, version, repo_name, build_args)


def run(args):
    repo_name = get_repo_name()
    version = get_project_version_no()

    if len(args) > 0:
        image = args[0]
        build_args = " ".join(args[1:])
        process_docker_image(image, version, repo_name, build_args)
    else:
        build_all_images("")


if __name__ == "__main__":
    args = sys.argv[1:]
    run(args)