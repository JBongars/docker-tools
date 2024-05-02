
#!/bin/bash

set -eu
set -o pipefail

download_target=$1
args=${@:2}

if [ -f $download_target ]; then
    rm $download_target
fi

mkdir /home/rpm

# dnf install -y --downloadonly --installroot=/home --downloaddir=/home/rpm $args --releasever=8.9 --setopt=install_weak_deps=false
dnf install -y --downloadonly --downloaddir=/home/rpm $args --releasever=8.9 --setopt=install_weak_deps=false
createrepo /home/rpm # add metadata about rpm packages by creating a mini repo
tar -C /home/rpm -czvf $download_target .

exit 0
