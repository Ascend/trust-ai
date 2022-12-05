# ai-tool-cfs

# 1.介绍
**口令加解密工具**

加密功能：使用本工具读入口令明文，通过白盒加密后写入指定文件。
解密功能：使用本工具(可指定文件目录),读取加密的口令内容，进行白盒解密，并返回明文口令。

## 注意
本工具白盒基于github开源白盒，存在一定安全风险。用户可选择性更换白盒组件。


# 2.安装教程
工具提供一键式安装脚本 `install.sh`。

其中，主要流程如下
1.  系统创建白盒表；
2.  将白盒表编译进工具中,之后即可使用工具 1)加密口令写入文件;2)解密口令。

注：工具自编译需要`go >= 1.17`，且能够链接至[OpenWhiteBox](https://github.com/OpenWhiteBox/AES)以下载开源白盒组件。
用户也可直接使用本仓库编译好的[二进制文件](https://gitee.com/ascend/trust-ai/releases)。

# 3.使用说明

1.  `./ai-tool-cfs enc xxxx`进行口令加密。在enc参数后面输入口令明文。默认将加密后的口令存在encrypted_code文件中。

```
[root@ubuntu root]# ./ai-tool enc plain_password
```

2.  从指定文件读取白盒加密后的口令，进行解密。

```
[root@ubuntu  root]# ./ai-tool dec path(optional)
```



