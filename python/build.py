import subprocess
import json
import os
import sys

def get_package_json():
    script_path = os.path.dirname(os.path.realpath(__file__))
    package_json_path = os.path.join(script_path, "package.json")

    with open(package_json_path) as f:
        return json.load(f)

def get_project_version_no():
    return get_package_json()["version"]

def get_repo_name():
    return get_package_json()["docker_repository"]

def build_docker_image(dockerfile_path, local_tag_name, build_args):
    subprocess.run(f"docker build -f {dockerfile_path} -t {local_tag_name} {build_args} ..", shell=True, check=True)

def tag_docker_image(current_tag, next_tag):
    subprocess.run(f"docker tag {current_tag} {next_tag}", shell=True, check=True)

def process_docker_image(image_name, version, repo_name, build_args):
    script_path = os.path.dirname(os.path.realpath(__file__))
    dockerfile_path = os.path.join(script_path, f"images/Dockerfile.{image_name}")

    local_tag_name = f"dtools_{image_name}:latest"
    tag_name = f"julien23/dtools_{image_name}:{version}"
    latest_tag_name = f"julien23/dtools_{image_name}:latest"
    
    build_docker_image(dockerfile_path, local_tag_name, build_args)
    tag_docker_image(local_tag_name, tag_name)
    tag_docker_image(local_tag_name, latest_tag_name)

def run():
    repo_name = get_repo_name()
    version = get_project_version_no()
    args = []
    build_args = ""

    if len(sys.argv) > 1:
        args = sys.argv[1:]
        build_args = " ".join(args)

    if len(args) > 0:
        process_docker_image(args[0], version, repo_name)
    else:
        # Call the function for each Docker image to build and tag
        process_docker_image("alpine_base", version, repo_name, build_args)
        process_docker_image("alpine_dind_base", version, repo_name, build_args)
        process_docker_image("ubuntu", version, repo_name, build_args)
        process_docker_image("golang", version, repo_name, build_args)
        process_docker_image("kube", version, repo_name, build_args)
        process_docker_image("aws", version, repo_name, build_args)
        process_docker_image("awskube", version, repo_name, build_args)
        process_docker_image("github_actions", version, repo_name, build_args)

if __name__ == "__main__":
    run()