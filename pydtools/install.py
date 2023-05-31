import os
import subprocess

def get_current_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_profile_path():
    if os.name == 'nt':
        powershell_profile_stdout = subprocess.run("powershell -Command \"echo $PROFILE\"", capture_output=True)
        return powershell_profile_stdout.stdout.decode('utf-8').strip()
    elif os.path.isfile(os.path.join(os.path.expanduser('~'), '.zshrc')):
        return os.path.expanduser('~/.zshrc')
    elif os.path.isfile(os.path.join(os.path.expanduser('~'), '.bashrc')):
        return os.path.expanduser('~/.bashrc')
    else:
        print('No shell configuration file found.')
        exit(1)

def read_file(path):
    if os.name == 'nt':
        with open(path, 'r', encoding='utf-16') as f:
            return f.read()
    else:
        with open(path, 'r') as f:
            return f.read()
        
def append_to_file(path, content):
    if os.name == 'nt':
        with open(path, 'a', encoding='utf-16') as f:
            f.write(content)
    else:
        with open(path, 'a') as f:
            f.write(content)

def get_alias_string():
    cwd = get_current_path()
    if os.name == 'nt':
        return f"function de {{ & python '{cwd}\\run.py' $args }}"
    else:
        return f"alias de=\"python -m {cwd}/run.py\""

def run():
    # Define the Docker tools alias text
    docker_tools_text = f'''
    # ----------
    # DOCKER TOOLS
    {get_alias_string()}
    # ----------
    '''

    print(docker_tools_text)

    # Get the path to the current user's PowerShell profile
    profile_path = get_profile_path()

    profile_string = read_file(profile_path)
    
    if docker_tools_text in profile_string:
        print('Docker tools is already installed.')
        return

    append_to_file(profile_path, docker_tools_text) 

    print('Docker tools has been installed.')

if __name__ == "__main__":
    run()