import os

def get_profile_path():
    if os.name == 'nt':
        return os.path.expanduser('~\\Documents\\WindowsPowerShell\\Microsoft.PowerShell_profile.ps1')
    elif os.path.isfile(os.path.join(os.path.expanduser('~'), '.zshrc')):
        return os.path.expanduser('~/.zshrc')
    elif os.path.isfile(os.path.join(os.path.expanduser('~'), '.bashrc')):
        return os.path.expanduser('~/.bashrc')
    else:
        print('No shell configuration file found.')
        exit(1)

def run():
    # Define the Docker tools alias text
    docker_tools_text = '''
    # ----------
    # DOCKER TOOLS
    Set-Alias -Name de -Value {0}\\run.py
    # ----------
    '''.format(os.path.abspath(os.path.dirname(__file__)))

    # Get the path to the current user's PowerShell profile
    profile_path = get_profile_path()

    # Check if the profile file already contains the Docker tools text
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