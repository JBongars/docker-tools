import os
import subprocess

def get_repo_name():
    repo_path = os.path.join(os.path.dirname(__file__), '..', '..')
    return subprocess.check_output(['npm', 'view', repo_path, 'docker_repository'], text=True).strip()

def get_images():
    repo_name = get_repo_name()
    return subprocess.check_output(['docker', 'images', f'--filter=reference={repo_name}/dtools_*', '--format', '{{.Repository}}:{{.Tag}}'], text=True).splitlines()

# Push each image to the Docker registry in parallel
def push_image(image):
    print(f'{image} is pushing...')
    subprocess.run(['docker', 'push', image], check=True)
    print(f'\r{image} done')

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