

import subprocess

def remove_all_images():
    find_command = "docker images --filter \"reference=*/dtools_*\" --format \"{{.Repository}}:{{.Tag}}\""
    images = subprocess.run(find_command).stdout

    print("deleting images: ", images)
    remove_command = f"docker rmi $({find_command})"

    err = subprocess.run(remove_command).stderr
    print(err)

if __name__ == "__main__":
    remove_all_images()