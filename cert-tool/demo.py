# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
from ssl_key import SSLKey


if __name__ == "__main__":
    demo = SSLKey(alg_id=1)
    pwd = "abcdefghijklmnopqrstuvwxyz1234567890qwertyuiop"
    cipher, csr = demo.generate(pwd)  # generate同时也会返回cipher(str)和csr(bytes)
    demo.parse_cipher_data(cipher, pwd)
