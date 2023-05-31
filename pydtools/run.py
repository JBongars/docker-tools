import sys
import docker

from pydtools.container import run as container
from pydtools import build, clean, install, push


def is_docker_in_env():
    try:
        client = docker.from_env()
        client.ping()
        return True
    except docker.errors.APIError:
        print("Docker is installed but not running.")
        return False
    except docker.errors.DockerException as e:
        print(e)
        print("WARNING: Docker may not be installed.")
        return True


def usage():
    help_message = '''
Usage: de <comand> <...args>
de r|run     = run a container with attached shell
de b|build   = build a container and tag it with <repo>/dtools-<container-name>
de c|clean   = remove all local instances of dtools containers
de install   = creates an alias in $PROFILE or .bashrc or .zshrc so you can all this script using "de"
de push      = pushes all local dtool containers to docker hub
    '''
    print(help_message)


def run():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    print(args)

    if not is_docker_in_env():
        sys.exit(1)

    command_mapping = {
        "r": container.run,
        "run": container.run,
        "b": build.run,
        "build": build.run,
        "c": clean.run,
        "clean": clean.run,
        "install": install.run,
        "push": push.run,
    }

    func = command_mapping.get(command)
    if func is not None:
        func(args)
    else:
        print(f"Invalid command: {command}")
        usage()


if __name__ == "__main__":
    run()