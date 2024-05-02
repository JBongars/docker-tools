import os
import subprocess

from .utils import get_dtools_image_name


def availalbe_containers():
    return {
        "insomnia": insomnia,
        "firefox": firefox,
        "playwright": playwright,
    }


def export_as_env(env_name, env_value):
    if os.name == 'nt':
        subprocess.run(f'powershell -Command "setx {env_name} {env_value}"',
                       shell=True,
                       check=True)
    else:
        subprocess.run(f'export {env_name}={env_value}',
                       shell=True,
                       check=True)


def get_display_env():
    if os.name == 'nt':
        powershell_command = "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'vEthernet (WSL)').IPAddress"
        wsl_port = subprocess.run(
            f'powershell -Command "{powershell_command}"',
            capture_output=True,
            text=True).stdout.rstrip('\n') + ":0.0"
        return wsl_port
    else:
        print('could not set port... not implemented')


def graphical_application(container, args_string, cmd=None):
    # display_ip = get_display_env()
    display_ip = "172.23.224.1:0.0"
    export_as_env("DISPLAY", display_ip)

    command = f"docker run -ti --rm -e DISPLAY={display_ip} {args_string} {container} {cmd}"
    print("command = ", command)
    subprocess.run(command, shell=True, check=True)


# TODO - add volume mounting for insomnia configuration
def insomnia(args_string):
    image_name = get_dtools_image_name("insomnia")
    graphical_application(image_name, f"--cap-add SYS_ADMIN {args_string}",
                          f"insomnia")


def firefox(args_string):
    image_name = get_dtools_image_name("firefox")
    graphical_application(image_name, args_string)


def playwright(args_string):
    image_name = get_dtools_image_name("playwright")
    graphical_application(image_name, args_string)
