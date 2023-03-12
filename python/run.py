import os
import subprocess
import sys
import signal
import argparse

def is_dood():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dood', action='store_true', help='enable dood mode')
    args, unknown = parser.parse_known_args()
    return args.dood, unknown

def stop_container(container_id):
    print("Stopping container...")
    subprocess.run(f"docker stop {container_id}", shell=True, check=True)

    print("Removing container...")
    subprocess.run(f"docker rm {container_id}", shell=True, check=True)
    
def safely_exec_container(container_id, exec_string):
    cleanup_flag = True
    
    def cleanup_handler(_signum, _frame):
        if cleanup_flag:
            stop_container(container_id)

    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGABRT):
        signal.signal(sig, cleanup_handler)

    subprocess.run(f"docker exec -it {container_id} {exec_string}", shell=True, check=True)
    stop_container(container_id)

    cleanup_flag = False

def run_docker_container(image_name, run_dood_string, run_dind_string, exec_dind_string="zsh"):
    
    if is_dood():
        # ugly patch to remove the --dood flag
        if "--dood " in run_dood_string:
            run_dood_string = run_dood_string.replace("--dood", "")
        subprocess.run(run_dood_string, shell=True, check=True)
        return

    subprocess.run(run_dind_string, shell=True, check=True)
    container_id = subprocess.check_output(f"docker ps -q -f ancestor={image_name}", shell=True).decode().strip().split("\n")[0]

    safely_exec_container(container_id, exec_dind_string)

def ubuntu(args_string):
    subprocess.run(f"docker run -ti -v {os.getcwd()}:/work --rm {args_string} ubuntu:latest bash", shell=True, check=True)

def dubuntu(args_string):
    subprocess.run(f"docker run -ti -v {os.getcwd()}:/work --rm {args_string} julien23/dtools_ubuntu:latest zsh", shell=True, check=True)

def dubuntu(args_string):
    subprocess.run(f"docker run -ti -v {os.getcwd()}:/work --rm {args_string} julien23/dtools_maven:latest zsh", shell=True, check=True)

def golang(args_string):
    subprocess.run(f"docker run -ti -v {os.getcwd()}:/work --rm {args_string} julien23/dtools_golang:latest zsh", shell=True, check=True)

def kube(args_string):
    image_name = "julien23/dtools_kube:latest"
    dood_command = f"docker run -ti -v {os.getcwd()}:/work --rm -v /var/run/docker.sock:/var/run/docker.sock {args_string} {image_name} zsh"
    dind_command = f"docker run -d -v {os.getcwd()}:/work --privileged {args_string} {image_name}"
    run_docker_container(image_name, dood_command, dind_command)

def aws(args_string):
    subprocess.run(f"docker run -it -v {os.getcwd()}:/work -v {os.path.expanduser('~')}/.aws:/root/.aws --rm {args_string} julien23/dtools_aws:latest zsh", shell=True, check=True)

def awskube(args_string):
    image_name = "julien23/dtools_awskube:latest"
    dood_command = f"docker run -it -v {os.getcwd()}:/work -v {os.path.expanduser('~')}/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock --rm {args_string} {image_name} zsh"
    dind_command = f"docker run -d -v {os.getcwd()}:/work -v {os.path.expanduser('~')}/.aws:/root/.aws --privileged {args_string} {image_name}"
    run_docker_container(image_name, dood_command, dind_command)

def github_actions(args_string):
    subprocess.run(f"docker run -ti -v {os.getcwd()}:/work {args_string} julien23/dtools_github_actions:latest /bin/sh", shell=True, check=True)

def run():
    if len(sys.argv) == 1:
        print("Please specify a function to call as an argument.")
    else:
        function_name = sys.argv[1]
        args_string = " ".join(sys.argv[2:])

        if function_name in globals():
            globals()[function_name](args_string)
        else:
            print(f"Function '{function_name}' not found.")

if __name__ == "__main__":
    run()