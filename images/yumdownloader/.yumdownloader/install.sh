
#!/bin/bash

set -eu
set -o pipefail

install_tar=$1

# if RHEL disable the subscription-manager
if [ -f /etc/redhat-release -a -f /etc/yum/pluginconf.d/subscription-manager.conf ]; then
    # back up the original subscription-manager
    cp /etc/yum/pluginconf.d/subscription-manager.conf /etc/yum/pluginconf.d/subscription-manager.conf.bak
    
    set +e
    subscription-manager config --rhsm.manage_repos=0
    subscription-manager config --rhsm.manage_subscription=0
    subscription-manager config --rhsm.auto_enable_yum_plugins=0
    set -e
fi

# sudo
mkdir -p /tmp/rpm
tar -C /tmp/rpm -xzvf $install_tar
(
    cd /tmp/rpm
    yum install -y --cacheonly --disablerepo=* *.rpm
)

# if RHEL restore the original subscription-manager
if [ -f /etc/redhat-release -a -f /etc/yum/pluginconf.d/subscription-manager.conf ]; then
    mv /etc/yum/pluginconf.d/subscription-manager.conf.bak /etc/yum/pluginconf.d/subscription-manager.conf
fi

exit 0