一、环境依赖
| 软件名称 | 版本        |
|------|-----------|
| go   | >=1.16.4   |
| zip  | >=11.6.35 |

二、安装部署

1.解压

`unzip Ascend-mindxdl-aiguard_plugin.zip`

目录结构如下：

```
aiguard_plugin/
├── aiguard-plugin
│   └── aiguard-plugin //设备插件二进制
├── edge_om
│   └── config
│       └── edge_user.json //运行后降权 配置文件
├── install.sh //安装脚本
├── limit_file
│   ├── cfs_profile //容器资源限制
│   └── seccomp_profile.json //容器系统调用限制
│   └── seccomp_profile_low_version.json //容器系统调用限制 适配低版本docker
└── service
    └── aiguard_plugin.service //系统服务文件


2.执行安装脚本 bash install.sh

```

三、注意事项

在ubuntu上启动部分低版本docker容器可能会报`syscall clone3: permission denied: unknown.`，建议参考`seccomp_profile_low_version.json`修改seccomp配置文件并启动容器，详细说明参考issue: https://gitee.com/ascend/trust-ai/issues/I63QE7?from=project-issue
