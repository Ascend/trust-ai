1.构建device-plugin bash `build_plugin.sh`
*build.sh文件内容见附录:*
2.构建如下目录

    
        run_plugin/
        |-- aiguard-plugin
        |   |-- aiguard-plugin
        |-- edge_om
        |   `-- config
            |       `-- edge_user.json
            `-- limit_file
                |-- sceccomp_profile.json
                |-- cfs_profile

edge_user.json为:

    {
    "changed": 0,
    "user": "{usr}",
    "group": "{group}",
    "uid": 1000,
    "gid": 1000
    }

3.构建dev_plugin为服务自启
创建aiguard_plugin.service文件并放到/etc/systemd/system目录下并执行

    systemctl enable /etc/systemd/system/aiguard_plugin.service
    systemctl start /etc/systemd/system/aiguard_plugin.service
*aiguard_plugin.service文件见附录*



附录1 aiguard_plugin.service

    [Unit]
    Description=Ascend aiguard device plugin
    
    [Service]
    ExecStartPre=/bin/bash -c "dos2unix /home/user/testplugin/run_plugin/limit_file/true_profile"
    ExecStart=/bin/bash -c "apparmor_parser -r -W /home/user/testplugin/run_plugin/limit_file/true_profile"
    ExecStartPre=/bin/bash -c "cp /home/user/testplugin/run_plugin/limit_file/ceccomp_profile.json /var/lib/kubelet/seccomp/profiles"
    ExecStartPost=/bin/bash -c "/home/user/testplugin/run_plugin/aiguard-plugin/aiguard-plugin"
    Restart=always
    RestartSec=2
    KillMode=process
    Type=forking
    
    [Install]
    WantedBy=multi-user.target 

附录3 build.sh

    #!/bin/bash
    # Perform  build k8s-device-plugin
    # Copyright(C) Huawei Technologies Co.,Ltd. 2022. All rights reserved.
    
    set -e
    CUR_DIR=$(dirname "$(readlink -f "$0")")
    TOP_DIR=$(realpath "${CUR_DIR}"/..)
    
    output_name="aiguard-plugin"
    os_type=$(arch)
    build_type=build
    
    export GO111MODULE="on"
    export GONOSUMDB="*"
    
    function build_plugin() {
        [ ! -d "${TOP_DIR}/output" ] && mkdir "${TOP_DIR}/output"
        cd "$TOP_DIR"/src/dev_plugin/src/plugin/cmd/aiguardplugin
        go mod tidy
        export CGO_ENABLED=1
        export CGO_CFLAGS="-fstack-protector-strong -D_FORTIFY_SOURCE=2 -O2 -fPIC -ftrapv"
        export CGO_CPPFLAGS="-fstack-protector-strong -D_FORTIFY_SOURCE=2 -O2 -fPIC -ftrapv"
        go build -buildmode=pie -ldflags " -buildid none     \
                -s   \
                -extldflags=-Wl,-z,relro,-z,now,-z,noexecstack" \
                -o "${output_name}"  \
                -trimpath
        ls "${output_name}"
        if [ $? -ne 0 ]; then
            echo "fail to find aiguard-plugin"
            exit 1
        fi
    }
    
    function mv_file() {
        mv "$TOP_DIR/src/dev_plugin/src/plugin/cmd/aiguardplugin/${output_name}"   "${TOP_DIR}"/output
    }
    
    function change_mod() {
        chmod 500 "${TOP_DIR}/output/${output_name}"
    }
    
    function main() {
      build_plugin
      mv_file
      change_mod
    }
    
    main
    
