import glob
import hashlib
import os
import subprocess
import sys

from .utils import attach_git, attach_work, getcwd, set_hostname


def get_local_dockerfile(path="."):
    files = []

    if os.path.isdir(path):
        files = glob.glob(f"{path}/Dockerfile*")
    else:
        files = glob.glob(f"{path}")

    if not files:
        return None

    if len(files) == 1:
        return files[0]

    print(f'Multiple Dockerfiles found...')
    for file in files:
        print(f'- {file}')

    # prefer Dockerfile.dev* over Dockerfile
    for file in files:
        if "Dockerfile.dev" in file:
            return file

    return files[0]


def run_local_container(path, args_string):
    dockerfile = get_local_dockerfile(path)

    if not dockerfile:
        print("No Dockerfile located in the current directory")
        sys.exit(1)

    print(f"Using Dockerfile {dockerfile}...")

    cwd = getcwd()
    id = hashlib.sha256(cwd.encode()).hexdigest()
    id_truncated = f"{id[:3]}-{id[-3:]}"

    container_hostname = f"dlocal-{id_truncated}"
    image_name = f"dlocal-{id}"

    print(f"Building image {image_name}...")
    subprocess.run(
        f"docker build {path} -f {dockerfile} -t {image_name}:latest")

    try:
        subprocess.run(
            f"docker run -it {attach_work()}  {set_hostname(container_hostname)} {attach_git()} --rm {args_string} {image_name}"
        )
    except:
        print(f"Container '{image_name}' exited or could not be run.")

    print('Cleaning up...')
    subprocess.run(f"docker rmi {image_name}")

    sys.exit(0)
