import subprocess


def get_images(cmd):
    result = subprocess.run(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)

    if result.returncode != 0:
        print("Error: " + result.stderr.decode("utf-8"))
        return

    images = result.stdout.decode("utf-8").splitlines()
    return images


def get_docker_find_command(pattern):
    return f"docker images --filter \"reference={pattern}\" --format \"" + "{{.Repository}}:{{.Tag}}\""


def get_all_images():
    find_remotes = get_docker_find_command("*/dtools_*")
    find_localremote = get_docker_find_command("dtools_*")
    find_local = get_docker_find_command("dlocal-*")

    return get_images(find_remotes) + get_images(
        find_localremote) + get_images(find_local)


def clean_environment():
    images = get_all_images()

    for image in images:
        print("Removing image: " + image)
        result = subprocess.run("docker rmi " + image,
                                stderr=subprocess.PIPE,
                                shell=True)

        if result.returncode != 0:
            print("Error: " + result.stderr.decode("utf-8"))


def run():
    clean_environment()


if __name__ == "__main__":
    run()