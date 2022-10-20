# 简介
## 功能描述
KMSAgent批量配置工具，用于批量配置KMSAgent服务。
## 环境要求
1. 仅支持root用户使用。
2. 工具所在环境的python>=3.7，ansible==2.11.9，openssl>=1.1.1n。
3. 环境搭建建议使用[ascend-deployer工具](https://gitee.com/ascend/ascend-deployer)部署，执行`./start_download.sh --os-list=<OS1>,<OS2>`进行系统依赖下载，将对应的npu的zip包放入ascend-deployer/resources目录，编辑inventory_file文件，参考下面的**批量配置**一节中的步骤。执行`./install.sh --install=sys_pkg,python,npu`进行环境部署，更多详情[参考链接](https://gitee.com/ascend/ascend-deployer/blob/master/README.md)。
4. 仅支持Ubuntu 18.04/20.04、CentOS7及Euler操作系统，x86_64和aarch64架构均支持
5. 运行环境时间需要校准到正确的UTC时间
## 批量配置
1. 基于密钥认证的ssh连接，本工具运行前请确认系统中未安装paramiko（ansible在某些情况下会使用paramiko，其配置不当容易引起安全问题）。配置其他设备的ip地址，编辑inventory_file文件，格式如下：

   ```
   [ascend]
   localhost ansible_connection='local'
   ip_address_1 ansible_ssh_user='root'
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
2. 单机配置KMSAgent服务可跳过上述批量配置步骤，执行`./kmsagent.sh --check --python-dir={python_dir}`可查看带配置设备的连通性，并检查所有设备的系统时间。由于证书的导入要求时间在一段区间内才能成功导入，该步骤会提示用户哪些环境需要修改系统时间才能成功导入KMSAgent证书。如果有不想修改系统时间的环境，请编辑inventory_file文件，将对应环境的配置删除，之后运行工具也不会对其进行配置。
3. 执行`./kmsagent.sh --modify --python-dir={python_dir}`进行系统时间的修改，该步骤会修改步骤2提示环境的系统时间。如果某些环境不修改时间，请删除相关配置。
4. 执行`./kmsagent.sh --aivault-ip={ip} --aivault-port={port} --cfs-port={port} --cert-op-param={param} --subject={param} --python-dir={python_dir}`进行批量配置。该步骤会生成CA证书，会要求用户输入ca.key的密钥（长度不能小于6位），并进行第二次确认，之后在生成kmsagent.pem时会再次要求用户输入ca.key的密钥。

## 参数说明

用户根据实际需要选择对应参数完成安装，命令为`./install.sh [options]`。
参数说明请参见下表，表中各参数的可选参数范围可通过执行`./install.sh --help`查看。

| 参数            | 说明                                                                                                                        |
| :-------------- | --------------------------------------------------------------------------------------------------------------------------- |
| --help  -h      | 查询帮助信息。                                                                                                              |
| --aivault-ip    | 指定aivault服务的ip地址。                                                                                                   |
| --aivault-port  | 指定aivault服务的端口。                                                                                                     |
| --cfs-port      | 指定cfs服务的端口。                                                                                                         |
| --cert-op-param | 指定kmsagent.csr的用户信息，参考格式：`"yanfabu\|chengdu\|sichuan\|Huawei\|CN"`。                                           |
| --check         | 检查环境，确保控制机安装好可用的python3、ansible等组件，并检查与待安装设备的连通性及设备的系统时间。                        |
| --modify        | 修改远程节点的系统时间到UTC时间。                                                                                           |
| --python-dir    | 指定安装了ansible的python路径，参考格式：`/usr/local/python3.7.5` 或 `/usr/local/python3.7.5/`,默认是/usr/local/python3.7.5 |
| --subject       | 设置CA请求的主题，参考格式：`"/CN=Example Root CA"`。                                                                       |
| --verbose       | 打印详细信息。                                                                                                              |

## 注意事项
1. 工具运行要求`python>=3.7`且`ansible==2.11.9`。手动python安装参考路径为/usr/local/python3.7.5,执行`pip3 install cryptography==3.3.2 ansible==2.11.9`安装ansible。先安装cryptography再安装ansible，直接安装可能会导致依赖冲突。建议使用ascend-deployer工具进行部署。
2. 生成ca.key时的密钥须符合组织的安全要求。
