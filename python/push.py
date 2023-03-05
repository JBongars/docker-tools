import os
import subprocess
import json

def get_package_json():
    script_path = os.path.dirname(os.path.realpath(__file__))
    package_json_path = os.path.join(script_path, "..", "package.json")

    with open(package_json_path) as f:
        return json.load(f)

def get_repo_name():
    return get_package_json()["docker_repository"]

def get_images():
    repo_name = get_repo_name()
    return subprocess.check_output(['docker', 'images', f'--filter=reference={repo_name}/dtools_*', '--format', '{{.Repository}}:{{.Tag}}'], text=True).splitlines()

# Push each image to the Docker registry in parallel
def push_image(image):
    print(f'{image} is pushing...')
    try:
        subprocess.run(['docker', 'push', image], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f'\r{image} done', flush=True)
    except subprocess.CalledProcessError as e:
        print(f'\r{image} failed: {e}', flush=True)

def run():
    images = get_images()
    try:
        from multiprocessing import Pool, cpu_count
        num_workers = min(len(images), cpu_count())
        with Pool(num_workers) as pool:
            pool.map(push_image, images)
    except ImportError:
        # multiprocessing not available, fall back to serial processing
        for image in images:
            push_image(image)

if __name__ == "__main__":
    run()