# 简介
## 功能描述
批量配置工具，用于配置aivault服务及批量安装haveged、批量配置KMSAgent服务。
## 环境要求
1. 仅支持root用户使用工具。
2. master节点即工具所在环境需要有网络，或者需要一个有网络的环境下载依赖。
3. 工具所在的环境需要安装python和ansible，且3.7<= python版本 <=3.9，python库cryptography==3.3.2，ansible-core==2.11.9。
4. 加密工具运行环境需要安装开源OpenSSL工具，且版本>=1.1.1n，并且<3.0.0。
5. 请确保待配置环境已经安装包含KMSAgent的驱动，安装好后，可以使用KMSAgent服务。
6. 确保所有待配置环境已经安装docker，且版本>=18.09。
7. 仅支持Ubuntu 18.04/20.04、CentOS8.2及Euler2.10操作系统，x86_64和aarch64架构均支持。
8. 请确保各节点的根目录有足够的磁盘空间以正常进行批量配置。
9. 运行环境时间需要校准到正确的UTC时间，执行`rm -f /etc/localtime && cp /usr/share/zoneinfo/UTC /etc/localtime`将主节点即本工具所在环境的时间设置为UTC时间，再参考命令`date -s '2022-10-24 00:00:00'`校准系统时间，请以实际情况进行校准。之后如果使用之前生成的证书进行批量配置时需确保主节点的当前时间在之前生成的证书的有效期内。
10. 从[昇腾镜像仓库](https://ascendhub.huawei.com/#/detail/ai-vault)拉取aivault镜像（只需要下载与aivault服务节点相同架构的镜像）,镜像拉取完成后进入工具的resources目录，执行`docker save ascendhub.huawei.com/public-ascendhub/ai-vault:{version} > aivault_aarch64.tar`或`docker save ascendhub.huawei.com/public-ascendhub/ai-vault:{version} > aivault_x86_64.tar`将镜像保存到工具的resources目录（请将**version**替换成对应的版本，镜像保存时的架构名需要一致）。
11. 请从[官网](https://gitee.com/ascend/trust-ai/releases)获取Ascend-mindxdl-aiguard_plugin_{version}_linux-{arch}.zip文件，然后将其放到工具的resources目录(可选)。

## 工具获取与安装
点击右上角“克隆/下载”按钮，然后点击下方“下载zip”，下载后将zip传到Linux环境上解压使用。建议解压zip包前将环境umask设置成077，并只放到/root目录下解压、使用工具。
如果Linux环境没有网络，用户可在有网络的Windows系统上（该系统须安装python，且3.7<= python版本 <= 3.9）解压zip包，然后双击**start_download.bat**文件进行依赖下载，下载完成后将整个工具传到Linux环境上进行批量配置。
## 批量配置
本工具运行前请确认系统中未安装paramiko（ansible在某些情况下会使用paramiko，其配置不当容易引起安全问题）。可使用基于密钥认证的ssh连接和账户密码的ssh连接方式，参考如下1-2步骤（使用其中一种方式即可，推荐基于密钥认证的ssh连接方式）。
1. 基于密钥认证的ssh连接，编辑inventory_file文件，配置其他设备的ip地址，其中aivault服务所在节点最多有一个，该节点不会进行KMSAgent配置，仅安装haveged、导入aivault镜像并启动aivault服务，该节点须配置变量server='aivault'。inventory_file文件格式如下：

   ```
   [ascend]
   localhost ansible_connection='local'
   ip_address_1 server='aivault'  # aivault服务所在节点
   ip_address_2
   ip_address_3
   ```

   设置密钥认证的参考操作如下，请用户注意ssh密钥和密钥密码在使用和保管过程中的风险，特别是密钥未加密时的风险，用户应按照所在组织的安全策略进行相关配置，包括并不局限于软件版本、口令复杂度要求、安全配置（协议、加密套件、密钥长度等，特别是/etc/ssh下和~/.ssh下的配置）：
   ```bash
   ssh-keygen -t rsa -b 3072   # 登录管理节点并生成SSH Key。安全起见，建议用户到"Enter passphrase"步骤时输入密钥密码，且符合密码复杂度要求。建议执行这条命令前先将umask设置为0077，执行完后再恢复原来umask值。
   ssh-copy-id -i ~/.ssh/id_rsa.pub <user>@<ip>   # 将管理节点的公钥拷贝到所有节点的机器上，<user>@<ip>替换成要拷贝到的对应节点的账户和ip。
   ```

2. 基于账号密码认证的ssh连接，编辑trust-ai/deployer/config/ansible.cfg文件，将**host_key_checking**的值改成False。然后编辑inventory_file文件，配置其他设备的ip地址，其中aivault服务所在节点最多有一个，该节点不会进行KMSAgent配置，仅安装haveged和导入aivault镜像并启动aivault服务，该节点须配置变量server='aivault'。inventory_file文件格式如下：

   ```
   [ascend]
   localhost ansible_connection='local'
   ip_address_1 ansible_ssh_pass='password' server='aivault'  # aivault服务所在节点
   ip_address_2 ansible_ssh_pass='password'
   ip_address_3 ansible_ssh_pass='password'
   ```

3. 默认5个并发数，如果待配置环境数量大于5，须修改trust-ai/deployer/config/ansible.cfg文件中的forks值，改成待配置的节点总数（可选）。
4. 执行`./`deploy.sh` --aivault-ip={ip} --python-dir={python_dir}`进行批量配置。该步骤会生成CA证书(之后使用工具时可将之前使用工具生成的命名为ca.key和ca.pem的文件放入resources/cert目录，然后指定`--include-cert`参数跳过证书生成，使用该方式进行批量配置时需确保主节点的当前时间在ca.pem证书的有效期内），会要求用户输入ca.key的密钥（长度不能小于6位，且不能大于64位），并进行第二次确认。程序启动后会对各节点的时间进行检测，如果有不满足条件的节点，会打印出来，并要求用户输入[y]es/[n]o进行确认，如果输入“y“或"yes”程序会修改不满足条件的节点的时间，如果输入“n”或“no”会终止程序。
5. 批量配置操作完成后，请删除inventory_file文件，避免安全风险。

## 参数说明

用户根据实际需要选择对应参数完成批量配置，命令为`./deploy.sh [options]`。
参数说明请参见下表，表中各参数的可选参数范围可通过执行`./deploy.sh --help`查看。

| 参数           | 说明                                                                                                                          |
| :------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| --help  -h     | 查询帮助信息。                                                                                                                |
| --aivault-ip   | 指定aivault服务的ip地址。                                                                                                     |
| --aivault-port | 指定aivault服务的端口，默认5001。                                                                                             |
| --cfs-port     | 指定cfs服务的端口，默认是1024。                                                                                               |
| --offline      | 离线模式，不会下载haveged，工具所在的环境没有网络时须指定。                                                              |
| --python-dir   | 指定安装了ansible的python路径，参考格式：`/usr/local/python3.7.5` 或 `/usr/local/python3.7.5/`,默认是/usr/local/python3.7.5。 |
| --all          | 所有节点执行kmsagent批量配置任务，默认master节点不进行配置。                                                                   |
| --include-cert | 证书存在时跳过证书生成。                                                                                                      |

## 注意事项
1. 生成ca.key时的密钥须符合组织的安全要求。
2. master节点不能是aivault服务所在节点。
3. 批量配置任务依赖master节点，请不要删除或注释掉master节点的配置。
