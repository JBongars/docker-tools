from .custom_containers import availalbe_containers as custom_containers
from .docker_based_containers import availalbe_containers as docker_based_containers
from .graphical_containers import availalbe_containers as graphical_containers


def get_available_containers():
    return {
        **custom_containers(),
        **docker_based_containers(),
        **graphical_containers()
    }
