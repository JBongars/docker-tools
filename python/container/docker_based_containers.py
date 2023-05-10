import argparse
import subprocess

from .run import safely_exec_container


def is_dood():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dood', action='store_true', help='enable dood mode')
    args, unknown = parser.parse_known_args()
    return args.dood, unknown


def run_docker_container(image_name,
                         run_dood_string,
                         run_dind_string,
                         exec_dind_string="zsh"):

    if is_dood():
        # ugly patch to remove the --dood flag
        if "--dood " in run_dood_string:
            run_dood_string = run_dood_string.replace("--dood", "")
        subprocess.run(run_dood_string, shell=True, check=True)
        return

    subprocess.run(run_dind_string, shell=True, check=True)
    container_id = subprocess.check_output(
        f"docker ps -q -f ancestor={image_name}",
        shell=True).decode().strip().split("\n")[0]

    safely_exec_container(container_id, exec_dind_string)
