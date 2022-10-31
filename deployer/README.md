# 简介
## 功能描述
KMSAgent批量配置工具，用于批量配置KMSAgent服务。
## 环境要求
1. 仅支持root用户使用工具。
2. 工具所在的环境即master节点需要安装python和ansible，且python>=3.7，python库cryptography==3.3.2，ansible-core==2.11.9。
3. 加密工具运行环境需要安装开源OpenSSL工具，且版本>=1.1.1n，并且<3.0.0。
4. 请确保待配置环境已经安装包含KMSAgent的驱动，安装好后，可以使用KMSAgent服务。
5. 确保工具所在环境已经安装docker，且版本>=18.09。
6. 仅支持Ubuntu 18.04/20.04、CentOS8.2及Euler2.10操作系统，x86_64和aarch64架构均支持。
7. 运行环境时间需要校准到正确的UTC时间。
8. 请确保各节点的根目录有足够的磁盘空间以正常进行批量配置。
## 批量配置
1. 基于密钥认证的ssh连接，本工具运行前请确认系统中未安装paramiko（ansible在某些情况下会使用paramiko，其配置不当容易引起安全问题）。配置其他设备的ip地址，编辑inventory_file文件，aivault服务所在节点不会进行KMSAgent配置，仅安装haveged、docker和导入ai-vault镜像，须配置变量server='aivault', 格式如下：

   ```
   [ascend]
   localhost ansible_connection='local'
   ip_address_1 ansible_ssh_user='root' server='aivault'  # aivault服务所在节点
   ip_address_2 ansible_ssh_user='root'
   ```

   设置密钥认证的参考操作如下，请注意ssh密钥和密钥密码在使用和保管过程中的风险，特别是密钥未加密时的风险，用户应按照所在组织的安全策略进行相关配置，包括并不局限于软件版本、口令复杂度要求、安全配置（协议、加密套件、密钥长度等，特别是/etc/ssh下和~/.ssh下的配置）：
   ```bash
   ssh-keygen -t rsa -b 3072   # 登录管理节点并生成SSH Key。安全起见，建议用户到"Enter passphrase"步骤时输入密钥密码，且符合密码复杂度要求。建议执行这条命令前先将umask设置为0077，执行完后再恢复原来umask值。
   ssh-copy-id -i ~/.ssh/id_rsa.pub <user>@<ip>   # 将管理节点的公钥拷贝到所有节点的机器上，<user>@<ip>替换成要拷贝到的对应节点的账户和ip。
   ssh <user>@<ip>   # 验证是否可以登录远程节点，<user>@<ip>替换成要登录的对应节点的账户和ip。验证登录OK后执行`exit`命令退出该ssh连接。
   ```

   注意事项: 请用户注意ssh密钥和密钥密码在使用和保管过程中的风险。

2. 设置ssh代理管理ssh密钥，避免工具批量配置操作过程中输入ssh密钥密码。设置ssh代理的参考操作如下：
   ```bash
   ssh-agent bash   # 开启ssh-agent的bash进程
   ssh-add ~/.ssh/id_rsa         # 向ssh-agent添加私钥
   ```

3. 默认5个并行进程数，如果待配置环境数量大于5，须修改ansible.cfg文件中的forks值，改成待配置的节点数。
4. 执行`./kmsagent.sh --check`测试待配置设备的连通性。确保所有设备都能正常连接，若存在设备连接失败情况，请检查该设备的网络连接和sshd服务是否开启。执行本步骤的命令除检查设备的连通性外还会检查所有设备的系统时间。
5. KMSAgent批量配置操作完成后，及时退出ssh代理进程，避免安全风险。
   ```bash
   exit   # 退出ssh-agent的bash进程
   ```
## KMSAgent批量配置流程
1. 执行`rm -f /etc/localtime && cp /usr/share/zoneinfo/UTC /etc/localtime`将主节点即本工具所在环境的时间设置为UTC时间，再参考命令`date -s '2022-10-13 12:00:00'`校准系统时间，请以实际情况进行校准。
2. 从[晟腾镜像仓库](https://ascendhub.huawei.com/#/index)拉取aivault镜像（镜像的架构与待配置的aivault环境的架构相同）,镜像拉取完成后进入工具的resources目录，执行`docker save ascendhub.huawei.com/public-ascendhub/ai-vault-arm:{version} > aivault_aarch64.tar`或`docker save ascendhub.huawei.com/public-ascendhub/ai-vault-x86:{version} > aivault_x86_64.tar`将镜像保存到工具的resources目录（请将**version**替换成对应的版本，只需要下载ai-vault服务节点相同架构的镜像）。
3. 请从[官网](https://gitee.com/ascend/trust-ai/releases)获取Ascend-mindxdl-aiguard_plugin_{version}_linux-{arch}.zip文件，然后将其放到工具的resources目录(可选)。
4. 执行`./kmsagent.sh --check --python-dir={python_dir}`可查看带配置设备的连通性，并检查所有设备的系统时间。由于证书的导入要求时间在一段区间内才能成功导入，该步骤会提示用户哪些环境需要修改系统时间才能成功导入KMSAgent证书。如果有不想修改系统时间的环境，请编辑inventory_file文件，将对应环境的配置删除，之后运行工具也不会对其进行配置。
5. 执行`./kmsagent.sh --modify --python-dir={python_dir}`进行系统时间的修改，该步骤会修改步骤2提示环境的系统时间。如果某些环境不修改时间，请删除相关配置。
6. 执行`./kmsagent.sh --aivault-ip={ip} --aivault-port={port} --cfs-port={port} --cert-op-param={param} --subject={param} --python-dir={python_dir}`进行批量配置。该步骤会生成CA证书，会要求用户输入ca.key的密钥（长度不能小于6位），并进行第二次确认，之后在生成kmsagent.pem时会再次要求用户输入ca.key的密钥。

## 参数说明

用户根据实际需要选择对应参数完成批量配置，命令为`./kmsagent.sh [options]`。
参数说明请参见下表，表中各参数的可选参数范围可通过执行`./kmsagent.sh --help`查看。

| 参数            | 说明                                                                                                                        |
| :-------------- | --------------------------------------------------------------------------------------------------------------------------- |
| --help  -h      | 查询帮助信息。                                                                                                              |
| --aivault-ip    | 指定aivault服务的ip地址。                                                                                                   |
| --aivault-port  | 指定aivault服务的端口。                                                                                                     |
| --cfs-port      | 指定cfs服务的端口。                                                                                                         |
| --cert-op-param | 指定kmsagent.csr的用户信息，参考格式：`"yanfabu\|chengdu\|sichuan\|Huawei\|CN"`。                                           |
| --check         | 检查环境，确保master节点安装好可用的python3、ansible等组件，并检查与待配置设备的连通性及设备的系统时间。                        |
| --modify        | 修改远程节点的系统时间到UTC时间。                                                                                           |
| --python-dir    | 指定安装了ansible的python路径，参考格式：`/usr/local/python3.7.5` 或 `/usr/local/python3.7.5/`,默认是/usr/local/python3.7.5。 |
| --remoteonly    | 仅远程节点执行kmsagent批量配置任务。                                                                                         |
| --subject       | 设置CA请求的主题，参考格式：`"/CN=Example Root CA"`。                                                                       |
| --verbose       | 打印详细信息。                                                                                                              |

## 注意事项
1. 生成ca.key时的密钥须符合组织的安全要求。
2. master节点不能是ai-vault服务所在节点。
3. 批量配置任务依赖master节点，请不要删除或注释掉master节点的配置。
