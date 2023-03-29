import sys
import container
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
        print("Docker is not installed.")
        return False

def usage():
    print('Usage: de <comand> <...args>')
    print('de run = run a container with attached shell')

if __name__ == "__main__":
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
    