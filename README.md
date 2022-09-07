1.下载代码后解压，进入build目录

2.执行

```
dos2unix build.sh
bash build.sh
```
在output目录下生成了Ascend-mindxdl-aiguard_plugin.zip文件，将此文件放到任意目录进行解压（如“/home/HwHiAiUser”）

`unzip Ascend-mindxdl-aiguard_plugin.zip`

目录结构如下：

```
run_plugin/
├── aiguard-plugin
│   └── aiguard-plugin
├── edge_om
│   └── edge_user.json
├── limit_file
│   ├── cfs_profile
│   └── sceccomp_profile.json
└── service
    └── aiguard_plugin.service
```
3.修改edge_user.json
edge_user.json为:

    {
    "changed": 0,
    "user": "{HwHiAiUser}",
    "group": "{HwHiAiUser}",
    "uid": 1000,
    "gid": 1000
    }

3.构建dev_plugin为服务自启
修改aiguard_plugin.service文件放到/etc/systemd/system目录下并执行

    systemctl enable /etc/systemd/system/aiguard_plugin.service
    systemctl start /etc/systemd/system/aiguard_plugin.service
*aiguard_plugin.service参考文件见附录*
附录1 aiguard_plugin.service

```
    [Unit]
    Description=Ascend aiguard device plugin
    
    [Service]
    ExecStartPre=/bin/bash -c "dos2unix /home/HwHiAiUser/testplugin/run_plugin/limit_file/true_profile"
    ExecStart=/bin/bash -c "apparmor_parser -r -W /home/HwHiAiUser/testplugin/run_plugin/limit_file/true_profile"
    ExecStartPre=/bin/bash -c "cp /home/HwHiAiUser/testplugin/run_plugin/limit_file/ceccomp_profile.json /var/lib/kubelet/seccomp/profiles"
    ExecStartPost=/bin/bash -c "/home/HwHiAiUser/testplugin/run_plugin/aiguard-plugin/aiguard-plugin"
    Restart=always
    RestartSec=2
    KillMode=process
    Type=forking
    
    [Install]
    WantedBy=multi-user.target 

```

