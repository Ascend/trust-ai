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
