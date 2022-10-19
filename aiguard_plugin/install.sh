#! /bin/bash
set -e
CUR_DIR=$(cd $(dirname $0);cd ..; pwd)
function run_service(){
    mkdir -p /var/lib/kubelet/seccomp/profiles
    cp -rf ${CUR_DIR}/aiguard_plugin /usr/local/bin/
    cp ${CUR_DIR}/aiguard_plugin/service/aiguard_plugin.service /etc/systemd/system
    dos2unix /usr/local/bin/aiguard_plugin/limit_file/cfs_profile || exit 1
    apparmor_parser -r -W /usr/local/bin/aiguard_plugin/limit_file/cfs_profile || exit 2
    cp /usr/local/bin/aiguard_plugin/limit_file/seccomp_profile.json /var/lib/kubelet/seccomp/profiles/
    systemctl enable /etc/systemd/system/aiguard_plugin.service
    systemctl start aiguard_plugin.service
}
function check(){
    count=`ps -ef |grep aiguard-plugin |grep -v "grep" |wc -l`
    if (($count < 1));then
        echo "aiguard plugin run failed"
        exit 3
    fi
}
function main(){
    run_service
    check
}

main