#!/bin/sh

script_dir=$(basename $0)
yum_repo_path="/etc/yum.repos.d/localrepo.repo"

echo "
[root@kast-repository iconuser]# cat /etc/yum.repos.d/localrepo.repo
[localrepo]
name=Local Repo
baseurl=file:///home/iconuser/rpm2
gpgcheck=0
enabled=1
" > /etc/yum.repos.d/localrepo.repo

echo '
Command:
dnf --disablerepo="*" --enablerepo="localrepo" install "$script_dir/*"
'
