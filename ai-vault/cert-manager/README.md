# cert-manager

#### 说明
cert-manager用于为用户自动签发cfs证书和私钥。签发需要用到CA证书和私钥，CA私钥口令通过ai-tool-cfs白盒加解密工具加密并存放在encrypted_password中。签发时自动通过白盒解密口令，需要用户输入CFS私钥的口令，满足复杂度要求。返回cfs.zip压缩包，包含CA证书、CFS通过AES加密后的私钥和证书。

#### 程序要求
需要保证python可调用OpenSSL。(python安装默认自带openssl模块。若编译安装python，请添加openssl参数)。

#### 使用说明
当前版本cert-manager仅提供自动签发CFS证书和私钥，并对私钥加密的功能。
请求接口：
`POST https://{{ip}}:{{port}}/certmanager/v1/getcert`

请求携带参数：
1. CommonName (必选，不能为空，长度小于64)
2. CountryName (可选，长度不超过2)
3. StateOrProvinceName (可选，长度小于64)
4. LocalityName (可选，长度小于64)
5. OrganizationName (可选，长度小于64)
6. OrganizationalUnitName (可选，长度小于64)
7. CfsPassword (必选，满足复杂度要求，长度40-64)


#### 注意
1. 口令需满足长度[40, 64], 且需要包含数字、大写字母、小写字母、特殊字符（至少包含四类中的两类）。
2. 白盒加解密工具ai-whitebox需要放到/home/AiVault/目录下，否则会出现路径查找错误；白盒加密后的口令文件encrypted_password放在.ai-vault文件夹中：
3. 实际运行时cert-manager会被复制到.ai-vault文件下运行。
```
├── .ai-vault
│   ├── ca.key
│   ├── ca.pem
│   ├── encrypted_password
│   ├── cert
│   │   ├── mgmt
│   │   │   ├── ca.pem
│   │   │   ├── hmac.json
│   │   │   ├── mgmt.csr
│   │   │   ├── mgmt.key
│   │   │   └── mgmt.pem
│   │   ├── server.key
│   │   ├── server.pem
│   │   └── svc
│   │       ├── ca.pem
│   │       ├── hmac.json
│   │       ├── svc.csr
│   │       ├── svc.key
│   │       └── svc.pem
├── ai-whitebox
└── cert-manager
    ├── config.py
    ├── log
    │   └── cert_manager_run.log
    ├── main
    │   ├── app.py
    │   └── view
    │       ├── cert_manager_view.py
    ├── __pycache__
    │   └── config.cpython-38.pyc
    ├── README.md
    ├── run.py
    └── utils
        ├── aes.py
        ├── log.py
        ├── ssl_key.py
        ├── status_code.py
        └── tools.py
```