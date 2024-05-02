import os
import glob
import subprocess
import json
import sys
import jinja2
import re
import shutil


def get_template_header(image_name="<template>"):
    return f"""
# THIS IS A GENERATED DOCKERFILE.
# TO CHANGE, PLEASE MODIFY ^/templates/{image_name}.dockerfile.j2
# AND RUN python ^/python/build.py {image_name}
# ------------

"""


def get_package_json():
    script_path = os.path.dirname(os.path.realpath(__file__))
    package_json_path = os.path.join(script_path, "..", "package.json")

    with open(package_json_path) as f:
        return json.load(f)


def get_project_version_no():
    return get_package_json()["version"]


def get_project_extension():
    return ".dockerfile.j2"


def get_project_path():
    script_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(script_path, ".."))


def get_template_path():
    script_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(script_path, "..", f"templates")
    return os.path.abspath(template_path)


def get_repo_name():
    return get_package_json()["docker_repository"]


def get_jinja2_env():
    jinja_path = get_template_path()
    return jinja2.Environment(loader=jinja2.FileSystemLoader(jinja_path))


def get_jinja2_template_path(image_name):
    template_path = os.path.join(get_template_path(), f"{image_name}.dockerfile.j2")
    if os.path.exists(template_path):
        return template_path
    return ""


def get_flag(flag, args):
    if flag in args:
        args.remove(flag)
        return True, args
    return False, args


def get_all_templates():
    extension = get_project_extension()
    image_paths = glob.glob(os.path.join(get_project_path(), f"templates/*{extension}"))
    return [os.path.basename(elem).replace(extension, "") for elem in image_paths]


def save_file_to_path_with_safe_newline(source_path, destination_path):
    try:
        if os.path.exists(destination_path):
            os.remove(destination_path)

        shutil.copyfile(source_path, destination_path)

        # subprocess.run(f"cp {source_path} {destination_path}",
        #                shell=True,
        #                check=True)
        # with open(source_path, "r", newline="\n") as src_file:
        #     with open(destination_path, "w", newline="\n") as dest_file:
        #         dest_file.write(src_file.read())
        return True
    except Exception as e:
        print(e)
        return False


def substitute_copy_paths(template, dockerfile_path, verbose):
    template_path = get_template_path()
    if verbose:
        print("template_path= ", template_path)

    # find all COPY statements
    pattern = r"COPY\s+((?:\S+/)*\S+)\s+(\S+)"
    matches = re.findall(pattern, template)

    # copy files and replace COPY statements
    for src, dest in matches:
        if verbose:
            print(f"copying {src} to {dest}...")

        src_path = os.path.join(template_path, src)
        dest_path = os.path.join(dockerfile_path, os.path.basename(dest))
        if verbose:
            print(f"src_path= {src_path} dest_path= {dest_path}")

        result = save_file_to_path_with_safe_newline(src_path, dest_path)
        if not result:
            print(f"failed to copy {src} to {dest}")
            sys.exit(1)

        template = template.replace(
            f"COPY {src} {dest}", f"COPY ./{os.path.basename(dest)} {dest}"
        )
    return template


def generate_docker_image(dockerfile_path, image_name, verbose):
    env = get_jinja2_env()
    extension = get_project_extension()
    template = env.get_template(f"{image_name:}{extension}")
    rendered_template = get_template_header(image_name) + template.render()

    if not os.path.exists(dockerfile_path):
        os.makedirs(dockerfile_path)

    rendered_template = substitute_copy_paths(
        rendered_template, dockerfile_path, verbose
    )

    with open(f"{dockerfile_path}/Dockerfile", "w") as f:
        f.write(rendered_template)


def build_docker_image(dockerfile_path, local_tag_name, build_args):
    subprocess.run(
        f"docker build -t {local_tag_name} {build_args} {dockerfile_path}",
        shell=True,
        check=True,
    )


def tag_docker_image(current_tag, next_tag):
    subprocess.run(f"docker tag {current_tag} {next_tag}", shell=True, check=True)


def process_docker_image(
    image_name, version, repo_name, build_args, verbose=False, dryrun=False
):
    # weird quirk where docker needs the relative path not the abs path to build containers
    dockerfile_path = os.path.join(get_project_path(), "images", image_name)

    if not os.path.exists(dockerfile_path):
        os.makedirs(dockerfile_path)
        if verbose:
            print(f"Directory {dockerfile_path} created")

    local_tag_name = f"dtools_{image_name}:latest"
    version_tag_name = f"{repo_name}/dtools_{image_name}:{version}"
    latest_tag_name = f"{repo_name}/dtools_{image_name}:latest"

    if get_jinja2_template_path(image_name) != "":
        generate_docker_image(dockerfile_path, image_name, verbose)
    else:
        print(f"Template for {image_name} not found... using image path as is.")

    if not dryrun:
        build_docker_image(dockerfile_path, local_tag_name, build_args)
        tag_docker_image(local_tag_name, version_tag_name)
        tag_docker_image(local_tag_name, latest_tag_name)


def run(args):
    print("args= ", args)

    repo_name = get_repo_name()
    version = get_project_version_no()
    verbose, args = get_flag("--verbose", args)
    dryrun, args = get_flag("--dryrun", args)

    print("args= ", args)

    build_args = ""
    image = ""

    if len(args) > 0:
        image = args[0]
        build_args = " ".join(args[1:])

    print("build_args= ", build_args)

    if image != "all" and len(args) > 0:
        build_args = " ".join(args[1:])
        return process_docker_image(
            image, version, repo_name, build_args, verbose, dryrun
        )

    images = get_all_templates()
    for i, image in enumerate(images):
        print(
            f"""--------------------------------
({i + 1} of {len(images)}) building {image}..."""
        )
        process_docker_image(image, version, repo_name, build_args, verbose, dryrun)

    print(
        """
--------------------------------
DONE"""
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    run(args)
