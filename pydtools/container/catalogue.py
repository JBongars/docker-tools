from pydtools.container import custom_containers
from pydtools.container import docker_based_containers
from pydtools.container import graphical_containers


def get_available_containers():
    return {
        **custom_containers.availalbe_containers(),
        **docker_based_containers.availalbe_containers(),
        **graphical_containers.availalbe_containers()
    }
