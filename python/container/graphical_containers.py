import os
import subprocess

from .utils import get_dtools_image_name


def availalbe_containers():
    return {
        "insomnia": insomnia,
        "firefox": firefox,
    }


def get_display_env():
    if os.name == 'nt':
        powershell_command = "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'vEthernet (WSL)').IPAddress"
        wsl_port = subprocess.run(
            f'powershell -Command "{powershell_command}"',
            capture_output=True,
            text=True).stdout.rstrip('\n') + ":0"
        return wsl_port
    else:
        print('could not set port... not implemented')


def graphical_application(container, args_string):
    display_ip = get_display_env()
    subprocess.run(
        f"docker run -ti --rm -e DISPLAY={display_ip} {args_string} {container}",
        shell=True,
        check=True)


# TODO - add volume mounting for insomnia configuration
def insomnia(args_string):
    image_name = get_dtools_image_name("insomnia")
    graphical_application(image_name, f"--cap-add SYS_ADMIN {args_string}")


def firefox(args_string):
    image_name = get_dtools_image_name("firefox")
    graphical_application(image_name, args_string)
