# ai-vault

## 镜像制作
1. 下载本仓库代码
2. 进入到ai-vault目录
3. 将对应架构aivault包中的lib文件夹和ai-vault二进制程序放到ai-vault代码目录
4. 执行`docker build -t {image_name}:{image_version} .`

## 环境依赖
1. 安装环境需安装docker
2. 安装环境需安装haveged工具增熵

## 安装教程
1. 将build/install.sh上传到待安装环境。

2. 将一键配置证书中生成的ca.pem和ca.key上传到install.sh同级目录的.ai-vault目录中。目录结构如下。
```
├─install.sh                # 安装脚本
└─.ai-vault
   ├─ca.pem                 # CA证书    
   └─ca.key                 # CA私钥
```
3. 执行安装命令
`bash install.sh`

## 规格
1. 用户规格：500（包含管理员）
2. 导入数据规格：50M
3. 密钥规格：单用户10个

## 限制
- 导入数据为高危操作，请管理员确认导入文件无误并且没有训练推理任务
- 安装会创建UID为9001，用户名为AiVault用户。请确认和当前环境无冲突



