# Docker Tools

## Author

Julien Bongars

## License

MIT Free and Open Source

## Updated On

2023-02-18

# Description

This package provides an easy way to create and configure Docker containers as developer environments. It includes a function to start an Ubuntu container and a script to customize container configuration via command-line arguments. This simplifies the process of setting up and managing containerized development environments.

# Requirements

- Installation of Docker
- Signed in to your AWS account on your local machine (if you are using AWS)

## Windows

- Cygwin installed and added to PATH
- winpty (cygwin version)

### Pros:

- Simplifies the process of setting up and configuring Docker containers as developer environments.
- Provides a user-friendly interface for running containers and customizing their configuration.
- Can be easily adapted to fit the needs of individual developers and development teams.
- Helps ensure consistent container configuration across different development environments.
- Allows for collaboration and sharing of container environments among developers.

### Cons:

- Requires some familiarity with Docker and command-line interfaces.
- May not be suitable for highly specialized or complex container configurations.
- Requires careful management of container resources to avoid performance issues.

# How to use this Repository

To quickly and easily set up a Docker container as a developer environment, run the ubuntu function and customize the container configuration using command-line arguments:

```powershell
de ubuntu -p 8000:8000 -v /path/to/host/dir:/path/to/container/dir
```

This command runs an Ubuntu container and maps port 8000 on the host to port 8000 in the container, and mounts the /path/to/host/dir directory on the host to the /path/to/container/dir directory in the container.

Use the ubuntu function to ensure consistent container configuration across different development environments:

```powershell
de ubuntu -p 8000:8000 -v /path/to/host/dir:/path/to/container/dir
```

This command will set up the container with the same configuration on different machines, making it easier to collaborate with other developers.

Monitor container resource usage using Docker commands such as docker stats to avoid performance issues and ensure efficient resource allocation:

```powershell
docker stats <container-id>
```

This command displays resource usage statistics for the specified container, such as CPU usage, memory usage, and network I/O.

To build custom containers for highly specialized or complex container environments, use Dockerfiles and Docker build commands. For example, to build a custom container for a Node.js development environment, you could create a Dockerfile with the following contents:

```docker
FROM node:14
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

Then, run the following command to build the custom container:

```powershell
docker build -t my-node-app .
```

This command builds the container from the Dockerfile in the current directory and tags it with the name my-node-app.

To use shared container environments among developers, share Docker images or Dockerfiles and use the docker run command to spin up those environments quickly and easily. For example, to run a shared Node.js development environment, you could run the following command:

```powershell
docker run -p 8000:8000 -v /path/to/host/dir:/path/to/container/dir my-node-app
```

This command runs a container with the my-node-app image, mapping port 8000 on the host to port 8000 in the container, and mounting the /path/to/host/dir directory on the host to the /path/to/container/dir directory in the container.

# Caveats

## Setting Up Git Credentials

When using Git with remote repositories like GitHub or GitLab, you may need to provide credentials to authenticate with the server. In some cases, you can use a username and password, but for security reasons, it's recommended to use a personal access token instead.

### Access Token

#### Obtaining an Access Token from GitHub

1. Go to your GitHub account settings.
2. Click on "Developer settings" in the left sidebar.
3. Click on "Personal access tokens".
4. Click on "Generate new token".
5. Give the token a name and select the scopes (permissions) you want the token to have.
6. Click on "Generate token".
7. Copy the generated token to a secure location. This token will be used for authentication in Git commands.

#### Obtaining an Access Token from Gitlab

1. Go to your GitLab account settings.
2. Click on "Access Tokens" in the left sidebar.
3. Give the token a name and select the scopes (permissions) you want the token to have.
4. Click on "Create personal access token".
5. Copy the generated token to a secure location. This token will be used for authentication in Git commands.

### How to Set Up .netrc for Git Authentication

The `.netrc` file is a configuration file used by Git to store authentication credentials for remote servers. Here's how to set it up to use your access token for authentication in Git commands.

#### On Your Host Machine

1. Open a terminal or command prompt.
2. Navigate to your home directory.

- Linux and macOS: `cd ~`
- Windows: `cd %USERPROFILE%`

3. Create a new .netrc file:

```bash
touch ~\.netrc
```

4. Open the .netrc file in a text editor and add the following lines:

```bash
machine HOSTNAME
login USERNAME
password TOKEN
```

Example:

```bash
machine github.com
login someuser@gmail.com
password ghp_aaasaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

5. Save the changes to the `.netrc` file and exit the text editor.
6. Set the file permissions to 604 to make it secure but available to the docker container:

```bash
chmod 604 .netrc
```

7. Update your `.gitconfig` file to use the .netrc file for authentication:

```
[user]
	email = <YOUR_EMAIL>
	name = <YOUR_NAME>
[credential]
	helper = netrc -d -v
```

Now, when you run Git commands on your host machine that require authentication with the Git server, Git will use the credentials in the .netrc file to authenticate.

### Graphical Application (with VcXsrv)

#### Installing VcXsrv (Windows)

1. Download the Installer

Navigate to the VcXsrv Windows X Server project page on SourceForge (https://sourceforge.net/projects/vcxsrv/).
Click the green "Download" button. This will automatically download the latest version of the installer.

2. Run the Installer

Locate the downloaded installer file (vcxsrv-64.1.20.x.x-setup.exe or similar, depending on the version).
Double-click the installer file to start the installation process.
Follow the Installation Wizard

4. Adding VcXsrv to Your Path

Find the location of your VcXsrv installation. It's typically installed in C:\Program Files\VcXsrv\, but it may be different depending on your specific setup.
Add this directory to you path (you can do so by going to Environment Variables > System Variables > Path > Edit > New and adding the directory to the list)

5. Option A: Running VcXsrv using x-launch

Open x-launch from the C:\Program Files\VcXsrv directory and open xlaunch.exe
Select "Multiple windows", Display number should be -1 and click "Next"
Select "Start no client" and click "Next"
Select "Disable access control" and click "Next" **Allow connection from WSL2**

5. Option B: Running running VcXsrv using config.xlaunch

Open the config.xlaunch file using xlaunch.exe.
If you are not sure how to do this, you can try typing the following command:

```powershell
& "C:\Program Files\VcXsrv\xlaunch.exe" ".\config.xlaunch"
```

Again, you need to make sure that the path to xlaunch.exe is correct for your system.

6. Set Up Your Firewall

The first time you run VcXsrv, your firewall may ask you whether you want to allow it to access your private and public networks. Choose the option that best fits your security needs.
Typically, you'll want to allow it to access your private network but not your public network.

#### Problem - Unauthorized

You see this error on the command line:

```bash
PS C:\development\docker-tools> de r insomnia

SUCCESS: Specified value was saved.
command =  docker run -ti --rm -e DISPLAY=172.23.224.1:0.0 --cap-add SYS_ADMIN  julien23/dtools_insomnia:latest
05:32:49.996 › Running version 2023.1.0
05:32:50.036 › [electron client protocol] FAILED to set default protocol 'insomnia://'
05:32:50.082 › [electron client protocol] the current executable is not the default protocol for 'insomnia://'
05:32:50.136 › [electron client protocol] the default application set for 'insomnia://' is 'insomnia.desktop
'
Authorization required, but no authorization protocol specified
[1:0516/053250.155831:ERROR:ozone_platform_x11.cc(239)] Missing X server or $DISPLAY
[1:0516/053250.155866:ERROR:env.cc(255)] The platform failed to initialize.  Exiting.
```

Solution:

You need to make sure your xlaunch is running with the correct configuration including disabling access control.
Another possibility is that you have a firewall blocking the connection. You can try disabling your firewall to see if that fixes the problem.

# Image Descriptions

## ubuntu

This container is based on the Ubuntu 16.04 LTS distribution and includes common development tools such as Python 3, Git, Vim, Zsh, and Jq. It also includes the Oh My Zsh shell framework and Docker is not installed by default.

## kube

This container includes the tools needed for working with Kubernetes clusters, including Kubectl, Helm, and Kubernetes Kind. It also includes Docker, but it has to be used with Docker outside of Docker (DooD).

## AWS

This container includes the AWS CLI, Terraform, and Ansible, which are commonly used tools for working with Amazon Web Services (AWS). It also includes Docker, but it has to be used with Docker outside of Docker (DooD).

## AWSKUBE

This container includes the AWS CLI, Terraform, Ansible, Kubectl, Helm, and Kubernetes Kind. It also includes Docker, but it has to be used with Docker outside of Docker (DooD).

All of these containers are built on top of julien23/dtools_ubuntu:latest, which includes additional development tools such as make, gcc, and gdb.

# Development

## Add Scripts to PROFILE for calling

### Powershell

```powershell
.\powershell\init.ps1
```

This will add an alias in $PROFILE and allow you to call these scripts using de

### Linux

```bash
.\linux\init.ps1
```

This will add an alias in either ~/.bashrc or ~/.zshrc and allow you to call these scripts using de

## Build all Images

Call the respective "build" script from folder. Will automatically tag with the version number located in package.json. If you want to fork this project and tag your own docker repository, you can change the `docker_repository` key value in package.json

## Push to Docker Hub / Any Docker Repo

Login to your Docker Hub. Make sure you build your images first, and push your images to the cloud. Automatically tags your images. You may need to run `docker rmi $(docker images | grep 'dtools_')` on Linux or `docker images | Select-String 'dtools_' | ForEach-Object { docker rmi $_.ToString().Split(' ')[2] }` on Powershell to purge all previously tagged images before uploading as this will push ALL tags to your Docker Repository
