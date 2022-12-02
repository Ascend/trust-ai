# cert-tool

#### 说明
cert-tool用于为cfs创建私钥以及csr。其中，私钥使用aes加密保存，因此需传入一个口令用于加密私钥。

#### 程序要求
需要保证python可调用OpenSSL。(python安装默认自带openssl模块。若编译安装python，请添加openssl参数)。

#### 使用说明
1. `from ssl_key import SSLKey` 生成SSLKey实例，进行私钥和CSR的创建
2. `generate(password, path)` 传入口令和存储路径(路径默认`"./"`)，将在路径下生成`server.key`与`server.csr`两个文件，其中key文件为利用口令加密的私钥密文。
3. `parse_cipher_data(cipher, password)` 传入密文和口令，解密出私钥。
4. 具体可见 `demo.py` 示例。

#### 注意
口令需满足长度[40, 64], 且需要包含数字、大写字母、小写字母、特殊字符（至少包含四类中的两类）。
