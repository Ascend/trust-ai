# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
from ssl_key import SSLKey


if __name__ == "__main__":
    demo = SSLKey(alg_id=1)
    # encrypt test
    pwd = "abcdefghijklmnopqrstuvwxyz1234567890qwertyuiop"
    demo.generate(pwd, file_path="./")

    # decrypt test
    with open("./server.key", "rb") as kf:
        cipher_data = kf.read()
    plain_private_key = demo.parse_cipher_data(cipher_data, pwd)
    print(plain_private_key)
