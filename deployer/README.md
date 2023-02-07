# deployer介绍

## 简介

批量部署工具，用于部署aivault服务及批量安装haveged、批量部署KMSAgent服务。支持Ubuntu 18.04/20.04、CentOS8.2、Euler2.10等操作系统，x86_64和aarch64架构均支持。

## 工具获取与安装

点击右上角“克隆/下载”按钮，然后点击下方“下载zip”，下载后将zip传到Linux环境上解压使用。建议解压zip包前将环境umask设置成077，并只放到/root目录下解压、使用工具。
如果Linux环境没有网络，用户可在有网络的Windows系统上（该系统须安装python，且3.7<= python版本 <= 3.9）解压zip包，然后双击**start_download.bat**文件进行依赖下载，下载完成后将整个工具传到Linux环境上进行批量部署。


### 环境要求

1. 除工具所在节点外的待部署节点已安装docker，且版本>=18.09。
2. 工具所在节点需要校准到正确的UTC时间。
3. 边缘节点已安装驱动、固件，且版本>=22.0.0。
4. 确保边缘节点根目录的剩余磁盘空间在1G以上，工具所在节点和aivault节点的根目录的剩余磁盘空间在5G以上。

### 批量部署

1. 获取容器部署的zip包文件。
2. 将zip包传到待部署环境上，执行`unzip deployer.zip`解压zip包到当前目录或执行`unzip deployer.zip -d exdir`解压zip到指定目录（将exdir替换为实际的目录）。
3. 进入解压后的目录，编辑**inventory_file**文件，配置待部署节点的ip地址，如果节点的IP后配置了变量**server='aivault'**，该节点被视为aivault服务节点,aivault服务节点最多有一个，该节点不会进行KMSAgent部署，仅安装haveged和导入aivault镜像并启动aivault服务。使用基于账号密码认证的ssh连接（**请确保所有远程节点配置的密码是正确的，否则程序会报错终止**），inventory_file文件格式如下：

   ```text
   [ascend]
   localhost ansible_connection='local'
   node_ip_1 ansible_ssh_pass='password' server='aivault'  # aivault服务节点
   node_ip_2 ansible_ssh_pass='password'                   # 边缘节点

   [ascend:vars]
   ansible_ssh_user='root'
   ```

   **注意事项**：
   - localhost是容器环境请不要有任何改动，从localhost下一行开始配置待部署节点，一个节点仅配置一行。
   - node_ip替换为实际部署节点的物理机ip地址，password替换为对应的root用户登录密码。
   - 请确保待部署节点允许密码登录。如果不允许，可将/etc/ssh/sshd_config文件里的PasswordAuthentication字段配置为yes并重启sshd服务，用完本工具后再禁止密码登录即可。

4. 执行`./start_service.sh`导入deployer镜像，并用deployer镜像启动容器，如果start_service.sh所在环境没有安装docker，会自动安装docker。
5. 执行`./deploy.sh --aivault-ip={ip}`进行批量部署,如果配置aivault节点，可省去指定aivault-ip。

### zip包构建流程

**该流程仅用于说明如何构建容器部署的zip包，如果使用做好的zip包，请忽略该流程**。

1. 以root身份登录Linux环境，将trust-ai工具上传到Linux环境的/root目录下进行解压。请确保该环境已安装docker，版本>=18.09，且环境上网络可用。
2. 进入trust-ai/deployer/tools目录，将trust-ai/deployer/inventory_file文件放入trust-ai/deployer/tools目录。
3. 从[docker下载网站](https://mirrors.huaweicloud.com/docker-ce/linux/static/stable/)下载和Linux环境相同架构的docker-20.10.21.tgz（推荐的docker版本），将下载的docker包放入trust-ai/deployer/tools目录。
4. 从[昇腾镜像仓库](https://ascendhub.huawei.com/#/detail/ai-vault)拉取两种架构的aivault镜像，从[昇腾镜像仓库](https://ascendhub.huawei.com/#/detail/deployer)拉取和Linux环境相同架构的deployer镜像。
5. 镜像拉完后，执行`docker save ascendhub.huawei.com/public-ascendhub/ai-vault:{version} > aivault_aarch64.tar`保存arm架构的aivault镜像，x86架构的镜像保存为aivault_x86_64.tar。执行`docker save ascendhub.huawei.com/public-ascendhub/deployer:{version} > deployer_aarch64.tar`保存arm架构的deployer镜像，x86架构的镜像保存为deployer_x86_64.tar。
6. 执行`tar -zcf aivault.tar aivault_*.tar`将两个架构的aivault镜像tar包压缩成一个aivault.tar包，执行`tar -zcf deployer.tar deployer_*.tar`将deployer_{arch}.tar包压缩成deployer.tar包，arch为架构类型。
7. 执行`rm -f aivault_*.tar deployer_*.tar && zip deployer_{arch}.zip *`命令获得容器部署的zip包。

**构建deployer镜像方法**：进入trust-ai/deployer/docker_image目录，将上述的aivault.tar放入当前目录，执行`DOCKER_BUILDKIT=1 docker build -t ascendhub.huawei.com/public-ascendhub/deployer:{version} .`，其中version与aivault的版本一样。


## 参数说明

用户根据实际需要选择对应参数完成批量部署，命令为`./deploy.sh [options]`。
参数说明请参见下表，表中各参数的可选参数范围可通过执行`./deploy.sh --help`查看。

| 参数                  | 说明                                                                                                                                                          |
| :-------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| --help  -h            | 可选，查询帮助信息。                                                                                                                                          |
| --aivault-ip          | 可选，指定aivault服务的ip地址，未配置aivault节点时必须指定。                                                                                                  |
| --svc-port            | 可选，指定aivault服务的端口，默认5001。                                                                                                                       |
| --mgmt-port           | 可选，指定管理aivault服务的服务器端口，默认9000。                                                                                                             |
| --cfs-port            | 可选，指定cfs服务的端口，默认是1024。                                                                                                                         |
| --online              | 可选，在线模式，默认离线模式。指定后会下载依赖，容器场景已内置依赖，不用指定该选项。                                                                          |
| --python-dir          | 可选，指定安装了ansible的python路径，参考格式：`/usr/local/python3.7.9` 或 `/usr/local/python3.7.9/`,默认是`/usr/local/python3.7.9`。容器场景请勿指定该选项。 |
| --all                 | 可选，所有节点执行kmsagent批量部署任务，默认master节点不进行kmsagent部署，容器场景请勿指定该选项。                                                            |
| --exists-cert         | 可选，证书存在时跳过证书生成，使用已有证书部署时须指定。                                                                                                      |
| --update-cert         | 可选，更新证书。                                                                                                                                              |
| --certExpireAlarmDays | 可选，证书到期提醒天数\[7-180](默认值90)。                                                                                                                    |
| --checkPeriodDays     | 可选，检查证书周期天数，范围为1到证书到期告警天数（默认值7）。                                                                                                |
| --maxKMSAgent         | 可选，连接KMSAgent的最大值（默认128）。                                                                                                                       |
| --maxLinkPerKMSAgent  | 可选，每个KMSAgent的链接最大值（默认值32）。                                                                                                                  |
| --maxMkNum            | 可选，mk编号的最大值（默认值10）。                                                                                                                            |
| --dbBackup            | 可选，ai-vault数据库备份文件保存地址。                                                                                                                        |
| --certBackup          | 可选，导入证书备份保存地址。                                                                                                                                  |
