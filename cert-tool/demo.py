# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
from ssl_key import SSLKey


if __name__ == "__main__":
    demo = SSLKey(alg_id=1)
    pwd = "abcdefghijklmnopqrstuvwxyz1234567890qwertyuiop"
    cipher_data, csr = demo.generate(pwd)  # cipher_data(str)和csr(bytes)

    plain_private_key = demo.parse_cipher_data(cipher_data, pwd)
