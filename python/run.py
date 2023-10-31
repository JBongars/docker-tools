import sys
import container.run as container
import build
import clean
import install
import push
import docker


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
de install   = creates an alias in $PROFILE or .bashrc or .zshrc so you can call this script using "de"
de push      = pushes all local dtool containers to docker hub
    '''
    print(help_message)


def run():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if not is_docker_in_env():
        sys.exit(1)

    if command in ["r", "run"]:
        container.run(args)
    elif command in ["b", "build"]:
        build.run(args)
    elif command in ["c", "clean"]:
        clean.run()
    elif command in ["install"]:
        install.run()
    elif command in ["push"]:
        push.run()
    else:
        print(usage())


if __name__ == "__main__":
    run()