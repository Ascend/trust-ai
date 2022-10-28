# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import re
import hashlib
import struct
import OpenSSL
import OpenSSL.crypto

from collections import namedtuple

from aes import AES


class SSLKey:
    """
    OpenSSL private key and csr
    """
    KEY_LEN = [16, 32]
    SALT_LEN = 16
    IV_LEN = 12

    def __init__(self, version: int = 1, alg_id: int = 0,iteration: int = 10000,
                 req_name: str = "CFS", req_country: str = "CN", req_state: str = "SC", req_city: str = "Chengdu",
                 req_organization: str = "HW", req_organization_unit: str = "Ascend", req_email: str = "address"):
        self.req_name = req_name
        self.req_country = req_country
        self.req_state = req_state
        self.req_city = req_city
        self.req_organization = req_organization
        self.req_organization_unit = req_organization_unit
        self.req_email = req_email

        self.version = version
        self.alg_id = alg_id
        self.iteration = iteration

        self.aes = None

    def _create_csr(self):
        """
        create private key and csr by OpenSSL
        Returns:

        """
        key = OpenSSL.crypto.PKey()
        key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
        req = OpenSSL.crypto.X509Req()
        req.get_subject().CN = self.req_name
        req.get_subject().C = self.req_country
        req.get_subject().ST = self.req_state
        req.get_subject().L = self.req_city
        req.get_subject().O = self.req_organization
        req.get_subject().OU = self.req_organization_unit
        req.get_subject().emailAddress = self.req_email
        req.set_pubkey(key)
        req.sign(key, 'sha256')

        private_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)

        csr = OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_PEM, req)

        return private_key, csr

    def _pbkdf2hash(self, password: str):
        if isinstance(password, str):
            password = password.encode()
        salt = os.urandom(self.SALT_LEN)
        work_key = hashlib.pbkdf2_hmac("sha256", password, salt, self.iteration, self.KEY_LEN[self.alg_id])
        return work_key, salt

    @staticmethod
    def passwd_check(password: str):
        _lower_character_reg = r'[a-z]{1,}'
        _upper_character_reg = r'[A-Z]{1,}'
        _number_reg = r'[0-9]{1,}'
        _special_character_reg = r'[!"#$%&\'()*+,-./:;<=>?@\[\]^_~{}|\\]{1,}'

        _passwd_complexity = [_lower_character_reg, _upper_character_reg, _number_reg, _special_character_reg]
        _passwd_reg = r'^[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@\[\]^_~{}|\\]{40,60}$'

        if re.match(_passwd_reg, password) is None:
            return False
        pwd_complex = 0
        for reg in _passwd_complexity:
            if re.search(reg, password) is not None:
                pwd_complex += 1
        if pwd_complex < 2:
            return False
        return True

    def generate(self, password: str):
        """
        generate the cipher private_key and csr
        cipher format:
        value:  version + alg_id + salt + iter_count + gcm_tag + iv + cipher_private_key
        length: 1         1        16     4            16        12   ...
        Args:
            password:

        Returns:

        """
        if len(password) < 40 or len(password) > 64:
            raise ValueError(f"password length wrong. Current length is {len(password)}, specified length [40, 60].")
        if not self.passwd_check(password):
            raise ValueError(f"password complexity wrong.")
        key, salt = self._pbkdf2hash(password)
        iv = os.urandom(self.IV_LEN)
        self.aes = AES(key, iv)
        plain_private_key, csr = self._create_csr()
        cipher_key, gcm_tag = self.aes.encrypt(plain_private_key)

        cipher_data = self.version.to_bytes(1, "little") + self.alg_id.to_bytes(1, "little") + salt + \
                      self.iteration.to_bytes(4, "little") + gcm_tag + iv + cipher_key

        return cipher_data, csr

    # def parse_cipher_data(self, cipher_data):
    #     """
    #
    #     Returns:
    #
    #     """
    #     CIPHER_FIELDS = namedtuple('ciphertext_fields',
    #                                ["version", "alg_id", "salt", "iter_count", "gcm_tag", "iv", "cipher_private_key"])
    #     STRUCT_FORMAT = ">1s1s16sI16s12s{}s".format(len(cipher_data) - 60)
    #
    #     cipher_data_



if __name__ == "__main__":
    test = SSLKey()
    pwd = "abcdefghijklmnopqrstuvwxyz1234567890qwertyuiop"
    a, b = test.generate(pwd)
    print(a)
    print(b)
