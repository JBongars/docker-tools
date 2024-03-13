import os
import subprocess
import codecs


def get_current_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_profile_path():
    if os.name == "nt":
        powershell_profile_stdout = subprocess.run(
            'powershell -Command "echo $PROFILE"',
            capture_output=True,
        )
        # check if the file exists
        if os.path.isfile(powershell_profile_stdout.stdout.decode("utf-8").strip()):
            return powershell_profile_stdout.stdout.decode("utf-8").strip()

        powershell_profile_stdout = subprocess.run(
            'powershell -Command "echo $PSHOME\\Profile.ps1"',
            capture_output=True,
        )

        if os.path.isfile(powershell_profile_stdout.stdout.decode("utf-8").strip()):
            return powershell_profile_stdout.stdout.decode("utf-8").strip()

        print("No PowerShell profile found.")
        exit(1)

    elif os.path.isfile(os.path.join(os.path.expanduser("~"), ".zshrc")):
        return os.path.expanduser("~/.zshrc")
    elif os.path.isfile(os.path.join(os.path.expanduser("~"), ".bashrc")):
        return os.path.expanduser("~/.bashrc")
    else:
        print("No shell configuration file found.")
        exit(1)


def get_file_encoding(path):
    with open(path, "rb") as f:
        raw = f.read(4)
    if raw.startswith(codecs.BOM_UTF8):
        return "utf-8-sig"
    if raw == b"\x00\x00\xFE\xFF":
        return "utf-32-be"
    if raw == b"\xFF\xFE\x00\x00":
        return "utf-32-le"
    if raw.startswith(b"\xFF\xFE"):
        return "utf-16-le"
    if raw.startswith(b"\xFE\xFF"):
        return "utf-16-be"
    return "utf-8"


def read_file(path):
    if os.name == "nt":
        encoding = get_file_encoding(path)
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    else:
        with open(path, "r") as f:
            return f.read()


def append_to_file(path, content):
    if os.name == "nt":
        encoding = get_file_encoding(path)
        with open(path, "a", encoding=encoding) as f:
            f.write(content)
    else:
        with open(path, "a") as f:
            f.write(content)


def get_alias_string():
    cwd = get_current_path()
    if os.name == "nt":
        return f"function de {{ & python '{cwd}\\run.py' $args }}"
    else:
        return f'alias de="python -m {cwd}/run.py"'


def run():
    # Define the Docker tools alias text
    docker_tools_text = f"""
    # ----------
    # DOCKER TOOLS
    {get_alias_string()}
    # ----------
    """

    print(docker_tools_text)

    # Get the path to the current user's PowerShell profile
    profile_path = get_profile_path()
    print("profile_path= ", profile_path)

    profile_string = read_file(profile_path)

    if docker_tools_text in profile_string:
        print("Docker tools is already installed.")
        return

    append_to_file(profile_path, docker_tools_text)

    print("Docker tools has been installed.")


if __name__ == "__main__":
    run()
