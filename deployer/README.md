# deployer介绍

## 简介

批量部署工具，用于部署aivault服务及批量安装haveged、批量部署KMSAgent服务。支持Ubuntu 18.04/20.04、CentOS8.2、Euler2.10等操作系统，x86_64和aarch64架构均支持。

## 工具获取与安装

点击右上角“克隆/下载”按钮，然后点击下方“下载zip”，下载后将zip传到Linux环境上解压使用。建议解压zip包前将环境umask设置成077，并只放到/root目录下解压、使用工具。
如果Linux环境没有网络，用户可在有网络的Windows系统上（该系统须安装python，且3.7<= python版本 <= 3.9）解压zip包，然后双击**start_download.bat**文件进行依赖下载，下载完成后将整个工具传到Linux环境上进行批量部署。

## 容器场景

### 容器场景环境要求

1. 除工具所在节点外的待部署节点已安装docker，且版本>=18.09。
2. 工具所在节点需要校准到正确的UTC时间。
3. 边缘节点已安装驱动、固件，且版本>=22.0.0。
4. 确保边缘节点根目录的剩余磁盘空间在1G以上，工具所在节点和aivault节点的根目录的剩余磁盘空间在5G以上。

### 容器场景批量部署

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

### 容器部署的zip包构建流程

**该流程仅用于说明如何构建容器部署的zip包，如果使用做好的zip包，请忽略该流程**。

1. 以root身份登录Linux环境，将trust-ai工具上传到Linux环境的/root目录下进行解压。请确保该环境已安装docker，版本>=18.09，且环境上网络可用。
2. 进入trust-ai/deployer/tools目录，将trust-ai/deployer/inventory_file文件放入trust-ai/deployer/tools目录。
3. 从[docker下载网站](https://mirrors.huaweicloud.com/docker-ce/linux/static/stable/)下载和Linux环境相同架构的docker-20.10.21.tgz（推荐的docker版本），将下载的docker包放入trust-ai/deployer/tools目录。
4. 从[昇腾镜像仓库](https://ascendhub.huawei.com/#/detail/ai-vault)拉取两种架构的aivault镜像，从[昇腾镜像仓库](https://ascendhub.huawei.com/#/detail/deployer)拉取和Linux环境相同架构的deployer镜像。
5. 镜像拉完后，执行`docker save ascendhub.huawei.com/public-ascendhub/ai-vault:{version} > aivault_aarch64.tar`保存arm架构的aivault镜像，x86架构的镜像保存为aivault_x86_64.tar。执行`docker save ascendhub.huawei.com/public-ascendhub/deployer:{version} > deployer_aarch64.tar`保存arm架构的deployer镜像，x86架构的镜像保存为deployer_x86_64.tar。
6. 执行`tar -zcf aivault.tar aivault_*.tar`将两个架构的aivault镜像tar包压缩成一个aivault.tar包，执行`tar -zcf deployer.tar deployer_*.tar`将deployer_{arch}.tar包压缩成deployer.tar包，arch为架构类型。
7. 执行`rm -f aivault_*.tar deployer_*.tar && zip deployer_{arch}.zip *`命令获得容器部署的zip包。

**构建deployer镜像方法**：进入trust-ai/deployer/docker_image目录，将上述的aivault.tar放入当前目录，执行`DOCKER_BUILDKIT=1 docker build -t ascendhub.huawei.com/public-ascendhub/deployer:{version} .`，其中version与aivault的版本一样。

## 物理机场景

### 物理机场景环境要求

1. 所有节点
   - 仅支持root用户使用。
   - 确保所有待部署环境已经安装docker，且版本>=18.09。
2. 部署工具节点
   - 工具所在环境需要有网络，或者需要一个有网络的环境下载依赖。
   - 确保根目录的剩余磁盘空间在5G以上。
   - 工具所在的环境需要安装python和ansible，且3.7<= python版本 <=3.9，安装python后执行`pip3 install setuptools==65.6.0 cryptography==3.3.2 ansible-core==2.11.9`安装相关依赖，python的安装路径作为参数`--python-dir`的值。
   - 工具运行需要开源OpenSSL工具，且版本>=1.1.1n，并且<3.0.0。
   - 部署工具节点需要校准到正确的UTC时间。执行`rm -f /etc/localtime && cp /usr/share/zoneinfo/UTC /etc/localtime`将环境的时间设置为UTC时间，再参考命令`date -s '2022-10-24 00:00:00'`校准系统时间，请以实际情况进行校准。之后如果使用之前生成的证书进行批量部署时需确保部署工具节点的当前时间在之前生成的证书的有效期内。
   - 要部署aivault节点时，从[昇腾镜像仓库](https://ascendhub.huawei.com/#/detail/ai-vault)拉取aivault镜像（只需要下载与aivault服务节点相同架构的镜像）。镜像拉取完成后进入工具的resources目录，执行`docker save ascendhub.huawei.com/public-ascendhub/ai-vault:{version} > aivault_aarch64.tar`或`docker save ascendhub.huawei.com/public-ascendhub/ai-vault:{version} > aivault_x86_64.tar`将镜像保存到工具的resources目录（请将**version**替换成对应的版本，镜像保存时的架构名需要一致）。
   - 如果要使用k8s，请从[官网](https://gitee.com/ascend/trust-ai/releases)获取Ascend-mindxdl-aiguard_plugin_{version}_linux-{arch}.zip文件，然后将其放到工具的resources目录，工具会在边缘节点上进行安装。
   - 如果部署工具节点要作为aivault节点或边缘节点，须额外满足相关节点的环境要求。

3. aivault节点
   - 确保根目录的剩余磁盘空间在5G以上。

4. 边缘节点
   - 请确保待部署环境已经安装包含KMSAgent的驱动，Atlas 500设备环境kmsagent可执行文件的位置是/home/data/miniD/driver/tools/kmsagent，其他设备的文件位置为/usr/local/Ascend/driver/tools/kmsagent
   - 确保根目录的剩余磁盘空间在1G以上。

### 物理机场景批量部署

本工具运行前请确认系统中未安装paramiko（ansible在某些情况下会使用paramiko，其配置不当容易引起安全问题）。EulerOS等很多操作系统默认禁止root用户远程连接，所以需提前配置/etc/ssh/sshd_config中PermitRootLogin为yes（个别OS配置方法或许不同，请参考OS官方说明）。批量部署任务依赖master节点，请不要删除或注释掉localhost节点的配置。可使用基于密钥认证的ssh连接和账户密码的ssh连接方式，参考如下1-2步骤（使用其中一种方式即可）。

1. 基于密钥认证的ssh连接。编辑trust-ai/deployer/config/ansible.cfg文件，将**host_key_checking**的值改成True。然后编辑inventory_file文件，配置其他节点的ip地址，其中aivault服务所在节点最多有一个，该节点不会进行KMSAgent部署，仅安装haveged、导入aivault镜像并启动aivault服务，该节点须配置变量server='aivault'。inventory_file文件格式如下：

   ```text
   [ascend]
   localhost ansible_connection='local' server='aivault' # aivault服务所在节点
   node_ip_2
   node_ip_3
   ```

   设置密钥认证的参考操作如下，请用户注意ssh密钥和密钥密码在使用和保管过程中的风险，特别是密钥未加密时的风险，用户应按照所在组织的安全策略进行相关配置，包括并不局限于软件版本、口令复杂度要求、安全配置（协议、加密套件、密钥长度等，特别是/etc/ssh下和~/.ssh下的配置）：

   ```bash
   ssh-keygen -t rsa -b 3072   # 登录管理节点并生成SSH Key。安全起见，建议用户到"Enter passphrase"步骤时输入密钥密码，且符合密码复杂度要求。建议执行这条命令前先将umask设置为0077，执行完后再恢复原来umask值。
   ssh-copy-id -i ~/.ssh/id_rsa.pub <user>@<ip>   # 将管理节点的公钥拷贝到所有节点的机器上，<user>@<ip>替换成要拷贝到的对应节点的账户和ip。
   ```

2. 基于账号密码认证的ssh连接（**请确保所有远程节点配置的密码是正确的，否则程序会报错终止**）。编辑inventory_file文件，配置其他节点的ip地址，其中aivault服务所在节点最多有一个，该节点不会进行KMSAgent部署，仅安装haveged和导入aivault镜像并启动aivault服务，该节点须配置变量server='aivault'。inventory_file文件格式如下：

   ```text
   [ascend]
   localhost ansible_connection='local' server='aivault'  # aivault服务所在节点
   node2_ip ansible_ssh_pass='password'
   node3_ip ansible_ssh_pass='password'
   ```

   **注意事项**：
   - 密码认证方式请确保待部署节点允许密码登录。如果不允许，可将/etc/ssh/sshd_config文件里的PasswordAuthentication字段配置为yes并重启sshd服务，用完本工具后再禁止密码登录即可。
   - 密码认证方式时请删除部署工具节点/root/.ssh目录里的内容。
   - 一个节点仅配置一行。

3. 默认50个并发数，最高并发数为255，如果待部署环境数量大于50（包含工具所在节点），可以修改trust-ai/deployer/config/ansible.cfg文件中的forks值，改成待部署的节点总数以加快部署速度（可选）。
4. 执行`./deploy.sh --aivault-ip={ip} --python-dir={python_dir}`进行批量部署。该步骤会生成CA证书(请确保生成ca.key时的密钥符合组织的安全要求），会要求用户输入ca.key的密码（长度不能小于6位，且不能大于64位），并进行第二次确认。程序启动后会对各节点的时间进行检测，如果有不满足条件的节点，会打印出来，并要求用户输入[y]es/[n]o进行确认，如果输入“y“或"yes”程序会修改不满足条件的节点的时间，如果输入“n”或“no”会终止程序。
5. 批量部署操作完成后，请删除inventory_file文件，避免安全风险。
6. 重新部署时，可以使用之前的证书（工具部署后resources/cert目录会有ca.key和ca.pem两个文件）进行部署。使用之前的证书进行部署时，须将之前部署生成的ca.key和ca.pem放入工具的resources/cert目录，且须额外指定`--exists-cert`参数。使用之前的证书进行批量部署时需确保部署工具节点的当前时间在ca.pem证书的有效期内，且要求输入密码时，须输入之前生成ca.key时的密码。（步骤6可选）。

## 参数说明

用户根据实际需要选择对应参数完成批量部署，命令为`./deploy.sh [options]`。
参数说明请参见下表，表中各参数的可选参数范围可通过执行`./deploy.sh --help`查看。

| 参数                  | 说明                                                                                                                                                      |
| :-------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| --help  -h            | 可选，查询帮助信息。                                                                                                                                      |
| --aivault-ip          | 可选，指定aivault服务的ip地址，未配置aivault节点时必须指定。                                                                                              |
| --svc-port            | 可选，指定aivault服务的端口，默认5001。                                                                                                                   |
| --mgmt-port           | 可选，指定管理aivault服务的服务器端口，默认9000。                                                                                                         |
| --cfs-port            | 可选，指定cfs服务的端口，默认是1024。                                                                                                                     |
| --online              | 可选，在线模式，默认离线模式。工具所在的环境有网络时指定可下载依赖，容器场景忽略该选项。                                                                  |
| --python-dir          | 可选，指定安装了ansible的python路径，参考格式：`/usr/local/python3.7.9` 或 `/usr/local/python3.7.9/`,默认是`/usr/local/python3.7.9`。容器场景忽略该选项。 |
| --all                 | 可选，所有节点执行kmsagent批量部署任务，默认master节点不进行kmsagent部署。                                                                                |
| --exists-cert         | 可选，证书存在时跳过证书生成。                                                                                                                            |
| --update-cert         | 可选，更新证书。                                                                                                                                          |
| --certExpireAlarmDays | 可选，证书到期提醒天数\[7-180](默认值90)。                                                                                                                |
| --checkPeriodDays     | 可选，检查证书周期天数，范围为1到证书到期告警天数（默认值7）。                                                                                            |
| --maxKMSAgent         | 可选，连接KMSAgent的最大值（默认128）。                                                                                                                   |
| --maxLinkPerKMSAgent  | 可选，每个KMSAgent的链接最大值（默认值32）。                                                                                                              |
| --maxMkNum            | 可选，mk编号的最大值（默认值10）。                                                                                                                        |
| --dbBackup            | 可选，ai-vault数据库备份文件保存地址。                                                                                                                    |
| --certBackup          | 可选，导入证书备份保存地址。                                                                                                                              |
