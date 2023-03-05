import os

def get_current_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_profile_path():
    if os.name == 'nt':
        return os.path.expanduser('~\\Documents\PowerShell\Microsoft.PowerShell_profile.ps1')
    elif os.path.isfile(os.path.join(os.path.expanduser('~'), '.zshrc')):
        return os.path.expanduser('~/.zshrc')
    elif os.path.isfile(os.path.join(os.path.expanduser('~'), '.bashrc')):
        return os.path.expanduser('~/.bashrc')
    else:
        print('No shell configuration file found.')
        exit(1)

def get_alias_string():
    cwd = get_current_path()
    if os.name == 'nt':
        return f"function de {{ & python {cwd}\\run.py $args }}"
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

    with open(profile_path, 'r') as f:
        profile_string = f.read()

    if docker_tools_text in profile_string:
        print('Docker tools is already installed.')
    else:
        with open(profile_path, 'a') as f:
            f.write(docker_tools_text)
        print('Docker tools has been installed.')

if __name__ == "__main__":
    run()