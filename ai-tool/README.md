# ai-tool

# 1.介绍
**交互式输入口令功能**

首先通过本工具将口令进行加密，并存储于环境变量中。 然后使用本工具启动cfs时即可读取环境变量中的口令密文并解密后交互式输入给cfs，达到一键启动功能。

**口令加解密功能**

加密功能：添加-p参数，使用本工具读入口令明文，通过白盒加密后输出加密后口令。<br />
解密功能：使用本工具(可指定文件目录),读取加密的口令内容，进行白盒解密，并返回明文口令。

## 注意
本工具白盒基于github开源白盒，存在一定安全风险。用户可选择性更换白盒组件。


# 2.安装教程
工具提供一键式安装脚本 `install.sh`。

其中，主要流程如下
1.  系统创建白盒表；
2.  将白盒表编译进工具中,之后即可使用工具 1)加密口令;2)解密口令;3)解密口令并启动cfs。

注：工具自编译需要`go >= 1.17`，且能够链接至[OpenWhiteBox](https://github.com/OpenWhiteBox/AES)以下载开源白盒组件。
用户也可直接使用本仓库编译好的[二进制文件](https://gitee.com/ascend/trust-ai/releases)。

# 3.使用说明
**交互式输入口令功能**
1.  `./ai-tool enc`进行口令加密。输入命令启动后终端会提示输入口令，此时需要在命令行中手动输入口令。

```
[root@ubuntu root]# ./ai-tool enc
please input psk password: 
please input cert password: 

```

2.  将输出的psk口令密文、cert口令密文分别存储在环境变量`PSK_KEY CERT_KEY`中,（可通过修改main.go中的`pskName\certName`变量自定义环境变量名）。

```
[root@ubuntu  root]# ./ai-tool enc
please input psk password: 
please input cert password: 
Please set environment variables: 
PSK_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CERT_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

3.  `./ai-tool run cfs_cmd`使用工具启动cfs命令，即可自动交互输入口令。
4. 打印工具帮助信息

```
[root@ubuntu root]# ./ai-tool h
```

**口令加解密功能**
1.  `./ai-tool enc -p xxxx`进行口令加密。在enc -p参数后面输入口令明文，返回口令密文内容。

```
[root@ubuntu root]# ./ai-tool enc -p plain_password
```

2.  `./ai-tool dec`从指定文件读取白盒加密后的口令，进行解密。默认从/home/AiVault/.ai-vault/encrypted_password中读取，如果指定path则从指定路径读取文件。

```
[root@ubuntu  root]# ./ai-tool dec path(optional)
```

3.  打印工具帮助信息

```
[root@ubuntu root]# ./ai-tool h
```