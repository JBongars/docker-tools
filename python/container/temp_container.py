import os
import subprocess

from .utils import get_dtools_image_name


def get_template_base_path(os):
    script_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_path, "../templates/modules/{os}/base.j2")


def get_base(os):
    base_path = get_template_base_path(os)
    with open(base_path) as f:
        return f.read()


def run_temp_container():
    base = get_base("ubuntu")

    print(base)
