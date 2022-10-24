# TrustAI

#### 描述
本项目主要包含AI-VAULT集成使用以及易用性工具开发参考。

#### 软件结构
```
├─ai-tool                   # 白盒加密PSK口令及容器中自动输入crypto_fs
├─ai-vault                  # AI-VAULT系统集成
│  ├─apigw                  # AI-VAULT网关参考设计    
│  ├─build                  # 安装运行脚本
│  ├─data-manager           # 数据迁移参考设计
│  ├─UI                     # 前端页面参考设计
│  ├─user-manager           # 用户管理参考设计
│  └─Dockerfile             # 镜像制作Dockerfile
├─aiguard_plugin            # fuse device及容器权限限制插件参考设计
└─kmsagent-deployer         # 批量依赖安装及配置工具参考设计
```

#### 介绍

- ai-tool

详细介绍见[ai-tool](./ai-tool/README.md)

- ai-vault

详细介绍见[ai-vault](./ai-vault/README.md)

- aiguard_plugin

详细介绍见[aiguard_plugin](./aiguard_plugin/README.md)

- kmsagent-deployer

详细介绍见[deploy](./kmsagent-deployer/README.md)

