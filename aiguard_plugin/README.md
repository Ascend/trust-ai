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
└── service
    └── aiguard_plugin.service //系统服务文件


2.执行安装脚本 bash install.sh
