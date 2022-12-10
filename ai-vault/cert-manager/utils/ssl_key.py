# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import re
import hashlib

from utils.aes import AES
from utils import status_code


class SSLKey:
    """
    OpenSSL private key and csr
    """
    KEY_LEN = [16, 32]
    SALT_LEN = 16
    IV_LEN = 12

    def __init__(self, version: int = 1, alg_id: int = 0, iteration: int = 10000,
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
        self.head_len = 22 + self.SALT_LEN + self.IV_LEN

        self.aes = None

    def _pbkdf2hash(self, password: str, salt: bytes = None):
        if isinstance(password, str):
            password = password.encode()
        if not salt:
            salt = os.urandom(self.SALT_LEN)
        work_key = hashlib.pbkdf2_hmac("sha256", password, salt, self.iteration, self.KEY_LEN[self.alg_id])
        return work_key, salt

    @staticmethod
    def _passwd_check(password: str):
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

    def encrypt_pri_key(self, pri_key: bytes, password: str):
        """
        use aes to encrypt pri_key
        cipher format:
        value: version + alg_id + salt + iter_count + gcm_tag + iv + cipher_private_key
        length:  1          1      16       4           16      12   ...
        Args:
            pri_key: private key
            password: password for encrypt private key
        Returns:
            cipher_text: cipher text for private key
         """
        if len(password) < 40 or len(password) > 64:
            return None, status_code.PASSWORD_ERROR
        if not self._passwd_check(password):
            return None, status_code.PASSWORD_ERROR
        work_key, salt = self._pbkdf2hash(password)
        iv = os.urandom(self.IV_LEN)
        self.aes = AES(work_key, iv)
        cipher_key, gcm_tag = self.aes.encrypt(pri_key)

        cipher_data = self.version.to_bytes(1, "little") + self.alg_id.to_bytes(1, "little") + salt + \
                      self.iteration.to_bytes(4, "little") + gcm_tag + iv + cipher_key
        return cipher_data, status_code.SUCCESS
