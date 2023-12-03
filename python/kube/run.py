import sys
import container.run as container


def usage():
    help_message = """
Usage: de kube <comand> <...args>
de kube r|run     = run a container with attached shell
"""
    print(help_message)


def run(args):
    if len(args) < 2:
        usage()
        sys.exit(1)

    command = args[0]
    args = args[1:]

    print(args)

    if command in ["r", "run"]:
        container.run(args)
    else:
        print(usage())


if __name__ == "__main__":
    run(sys.argv)
