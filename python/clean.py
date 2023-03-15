

import subprocess

def run():
    find_command = "docker images --filter \"reference=*/dtools_*\" --format \"{{.Repository}}:{{.Tag}}\""
    remove_command = f"docker rmi $({find_command})"

    err = subprocess.run(remove_command).stderr
    print(err)

if __name__ == "__main__":
    run()