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
1. 将trust-ai/ai-vault/build/install.sh上传到待安装环境。
2. 参考trust-ai/ai-tool获取ai-tool文件，生成加密后的口令文件encrypted_password，参考命令如下:
```
ai-tool_aarch64 enc -p ${passwd} > encrypted_password
```
3.编辑openssl.cnf文件，文件内容如下:
```
[v3_ca]
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
basicConstraints = critical,CA:true
keyUsage = cRLSign, keyCertSign
```
生成ca.pem、ca.key, 命令如下:
```
openssl genrsa -passout pass:${passwd} -aes256 -out ca.key 4096 2>/dev/null
openssl req -new -key ca.key -subj "/CN=Aiguard Root CA" -out ca.csr -passin pass:${passwd}
openssl x509 -req -in ca.csr -signkey ca.key -days 3650 -extfile openssl.cnf -extensions v3_ca -out ca.pem -passin pass:${passwd} 2>/dev/null
```
4. 将上述生成的ca.pem、ca.key以及ai-tool二进制白盒加密后的口令文件encrypted_password上传到install.sh同级目录的.ai-vault目录中。目录结构如下。
```
├─install.sh                # 安装脚本
└─.ai-vault
   ├─ca.pem                 # CA证书    
   ├─ca.key                 # CA私钥
   └─encrypted_password     # 加密后的口令文件
```
5. 执行安装命令
`bash install.sh --option=[option]`，安装脚本可接收多个参数，例如`bash install.sh --image=ascendhub.huawei.com/public-ascendhub/ai-vault:0.0.1-arm64 --svc-port=5001 --mgmt-port=9000`。参数说明如下表。
```
| 参数                  | 说明                                                           
| :------------         | ------------------------------------------------------------ |
| --image               | 必选，指定镜像名及tag。                                          
| --svc-port            | 可选，指定aivault服务的端口，默认5001。                                
| --mgmt-port           | 可选，指定管理aivault服务的服务器端口，默认9000。                        
| --update-cert         | 可选，更新证书。                                                     
| --certExpireAlarmDays | 可选，证书到期提醒天数[7-180](默认值90)。                               
| --checkPeriodDays     | 可选，检查证书周期天数，范围为1到证书到期告警天数（默认值7）。                
| --maxKMSAgent         | 可选，连接KMSAgent的最大值（默认128）。                                 
| --maxLinkPerKMSAgent | 可选，每个KMSAgent的链接最大值（默认值32）。                             
| --maxMkNum            | 可选，mk编号的最大值（默认值10）。                                      
| --dbBackup            | 可选，ai-vault数据库备份文件保存地址。                                  
| --certBackup          | 可选，导入证书备份保存地址。                                        
```

## 升级
升级前请停止对应的容器，然后按照安装步骤重新执行

## 规格
1. 用户规格：500（包含管理员）
2. 导入数据规格：50M
3. 密钥规格：单用户10个

## 限制
- 导入数据为高危操作，请管理员确认导入文件无误且已备份，并且当前没有训练推理任务
- 安装会创建UID为9001，用户名为AiVault用户。请确认和当前环境无冲突



