import sys
import container
import build
import clean
import install
import push

def usage():
    print('Usage: de <comand> <...args>')
    print('de run = run a container with attached shell')

if __name__ == "__main__":
    command = sys.argv[1]
    args = sys.argv[2:]

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
    