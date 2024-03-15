
#!/bin/bash

set -eu
set -o pipefail

download_target=$1
args=${@:2}

if [ -f $download_target ]; then
    rm $download_target
fi

mkdir /home/rpm

# yum install -y --downloadonly --installroot=/home --downloaddir=/home/rpm $args --releasever=8.9 --setopt=install_weak_deps=false
yum install -y --downloadonly --downloaddir=/home/rpm $args --releasever=8.9 --setopt=install_weak_deps=false
tar -C /home/rpm -czvf $download_target .

exit 0