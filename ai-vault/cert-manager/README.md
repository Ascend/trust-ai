# cert-manager

#### 说明
cert-manager用于为用户自动签发cfs证书和私钥。签发需要用到CA证书和私钥，CA私钥口令通过ai-tool-cfs白盒加解密工具加密并存放在encrypted_password中。签发时自动通过白盒解密口令，需要用户输入CFS私钥的口令，满足复杂度要求。返回cfs.zip压缩包，包含CA证书、CFS通过AES加密后的私钥和证书。

#### 程序要求
需要保证python可调用OpenSSL。(python安装默认自带openssl模块。若编译安装python，请添加openssl参数)。

#### 使用说明
当前版本cert-manager仅提供自动签发CFS证书和私钥，并对私钥加密的功能。
请求接口：
`POST http://{{ip}}:{{port}}/certmanager/v1/getcert`

请求携带参数：
1. CommonName (必选，不能为空，长度小于64)
2. CountryName (可选，长度小于64)
3. StateOrProvinceName (可选，长度小于64)
4. LocalityName (可选，长度小于64)
5. OrganizationName (可选，长度小于64)
6. OrganizationalUnitName (可选，长度小于64)
7. CfsPassword (必选，满足复杂度要求，长度40-64)


#### 注意
口令需满足长度[40, 64], 且需要包含数字、大写字母、小写字母、特殊字符（至少包含四类中的两类）。
白盒加解密工具ai-whitebox需要放到/home/AiVault/cert目录下，否则会出现路径查找错误；白盒加密后的口令文件encrypted_password也存放在该文件夹中：
```
.
├── ai-whitebox
│   ├── ai-whitebox
│   ├── common
│   │   ├── utils
│   │   │   └── common.go
│   │   └── whitebox
│   │       ├── api.go
│   │       └── encrypt_base.go
│   ├── generate.go
│   ├── go.mod
│   ├── go.sum
│   ├── install.sh
│   ├── main.go
│   └── README.md
├── cert
│   ├── ai-whitebox
│   ├── ca.csr
│   ├── ca.key
│   ├── ca.pem
│   ├── encrypted_password
│   └── tmp
└── cert-manager
    ├── config.py
    ├── log
    │   └── cert_manager_run.log
    ├── main
    │   ├── app.py
    │   ├── __pycache__
    │   │   └── app.cpython-38.pyc
    │   └── view
    │       ├── cert_manager_view.py
    │       └── __pycache__
    │           └── cert_manager_view.cpython-38.pyc
    ├── __pycache__
    │   └── config.cpython-38.pyc
    ├── README.md
    ├── run.py
    └── utils
        ├── aes.py
        ├── log.py
        ├── __pycache__
        │   ├── aes.cpython-38.pyc
        │   ├── log.cpython-38.pyc
        │   ├── ssl_key.cpython-38.pyc
        │   ├── status_code.cpython-38.pyc
        │   └── tools.cpython-38.pyc
        ├── ssl_key.py
        ├── status_code.py
        └── tools.py

```
