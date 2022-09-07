一、环境依赖
| 软件名称 | 版本        |
|------|-----------|
| go   | >=1.10    |
| zip  | >=11.6.35 |

二、安装部署

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
│   └── aiguard-plugin //挂载设备文件
├── edge_om
│   └── config
│       └── edge_user.json //运行后降权
├── limit_file
│   ├── cfs_profile //容器限制
│   └── seccomp_profile.json //容器限制
└── service
    └── aiguard_plugin.service //系统服务文件


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

3.创建log文件路径`/var/alog/AtlasEdge_log/aiguard_plugin/ `. seccomp路径`/var/lib/kubelet/seccomp/profiles`

4.构建dev_plugin为服务自启
修改aiguard_plugin.service文件放到/etc/systemd/system目录下并执行

    systemctl enable /etc/systemd/system/aiguard_plugin.service
    systemctl start /etc/systemd/system/aiguard_plugin.service
*aiguard_plugin.service参考如下*
```
    [Unit]
    Description=Ascend aiguard device plugin
    
    [Service]
    ExecStartPre=/bin/bash -c "dos2unix /home/HwHiAiUser/testplugin/run_plugin/limit_file/cfs_profile"
    ExecStart=/bin/bash -c "apparmor_parser -r -W /home/HwHiAiUser/testplugin/run_plugin/limit_file/cfs_profile"
    ExecStartPre=/bin/bash -c "cp /home/HwHiAiUser/testplugin/run_plugin/limit_file/seccomp_profile.json /var/lib/kubelet/seccomp/profiles"
    ExecStartPost=/bin/bash -c "/home/HwHiAiUser/testplugin/run_plugin/aiguard-plugin/aiguard-plugin"
    Restart=always
    RestartSec=2
    KillMode=process
    Type=forking
    
    [Install]
    WantedBy=multi-user.target 

```

