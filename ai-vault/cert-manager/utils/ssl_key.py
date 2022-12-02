# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import re
import hashlib
import struct
import OpenSSL
import OpenSSL.crypto
from collections import namedtuple

from utils.aes import AES


class SSLKey:
    """
    OpenSSL private key and csr
    """
    KEY_LEN = [16, 32]
    SALT_LEN = 16
    IV_LEN = 12

    KEY_NAME = 'server.key'
    CSR_NAME = 'server.csr'

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

    def _create_csr(self):
        """
        create private key and csr by OpenSSL
        Returns:
            private_key： private key
            csr: csr
        """
        key = OpenSSL.crypto.PKey()
        key.generate_key(OpenSSL.crypto.TYPE_RSA, 3072)
        req = OpenSSL.crypto.X509Req()
        req.get_subject().commonName = self.req_name
        req.get_subject().countryName = self.req_country
        req.get_subject().stateOrProvinceName = self.req_state
        req.get_subject().localityName = self.req_city
        req.get_subject().organizationName = self.req_organization
        req.get_subject().organizationalUnitName = self.req_organization_unit
        req.get_subject().emailAddress = self.req_email
        req.set_pubkey(key)
        req.sign(key, 'sha256')

        private_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)

        csr = OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_PEM, req)

        return private_key, csr

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

    def _write_file(self, key_text: bytes, csr_text: bytes, path: str):
        """
        Write cipher_key and csr to file.
        If file exists, this func will overwrite the file.
        Args:
            key_text: cipher key text
            csr_text: csr text
            path: file path
        """
        key_path = os.path.join(path, self.KEY_NAME)
        csr_path = os.path.join(path, self.CSR_NAME)
        with open(key_path, 'wb') as kf:
            kf.write(key_text)

        with open(csr_path, 'wb') as cf:
            cf.write(csr_text)

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
            raise ValueError(f"password length wrong. Current length is {len(password)}, specified length [40, 60].")
        if not self._passwd_check(password):
            raise ValueError(f"password complexity wrong")
        work_key, salt = self._pbkdf2hash(password)
        iv = os.urandom(self.IV_LEN)
        self.aes = AES(work_key, iv)
        cipher_key, gcm_tag = self.aes.encrypt(pri_key)

        cipher_data = self.version.to_bytes(1, "little") + self.alg_id.to_bytes(1, "little") + salt + \
                      self.iteration.to_bytes(4, "little") + gcm_tag + iv + cipher_key
        return cipher_data

    def generate(self, password: str, file_path="./"):
        """
        generate the cipher private_key and csr
        cipher format:
        value:  version + alg_id + salt + iter_count + gcm_tag + iv + cipher_private_key
        length: 1         1        16     4            16        12   ...
        Args:
            password: password for encrypt private key
            file_path: key and csr file path
        Returns:
            cipher_text: cipher text for private key
            csr: csr text
        """
        if len(password) < 40 or len(password) > 64:
            raise ValueError(f"password length wrong. Current length is {len(password)}, specified length [40, 60].")
        if not self._passwd_check(password):
            raise ValueError(f"password complexity wrong.")
        if not os.path.exists(file_path):
            raise ValueError(f"file path '{file_path}' is not exist.")
        work_key, salt = self._pbkdf2hash(password)
        iv = os.urandom(self.IV_LEN)
        self.aes = AES(work_key, iv)
        plain_private_key, csr = self._create_csr()
        cipher_key, gcm_tag = self.aes.encrypt(plain_private_key)

        cipher_data = self.version.to_bytes(1, "little") + self.alg_id.to_bytes(1, "little") + salt + \
                      self.iteration.to_bytes(4, "little") + gcm_tag + iv + cipher_key

        self._write_file(cipher_data, csr, file_path)

    def parse_cipher_data(self, cipher_bytes: bytes, password: str):
        """
        parse the key from cipher
        Args:
            cipher_bytes: cipher text for private key
            password: password for encrypt private key
        Returns:

        """
        cipher_fields = namedtuple('ciphertext_fields',
                                   ["version", "alg_id", "salt", "iter_count", "gcm_tag", "iv", "cipher"])
        struct_format = f"<1s1s16sI16s12s{len(cipher_bytes) - self.head_len}s"

        cipher_bytes_dict = cipher_fields(*struct.unpack(struct_format, cipher_bytes))
        if self.alg_id != int.from_bytes(cipher_bytes_dict.alg_id, "little"):
            raise ValueError("cipher header alg_id error")
        if self.iteration != cipher_bytes_dict.iter_count:
            raise ValueError("cipher header iteration error")
        work_key, _ = self._pbkdf2hash(password, cipher_bytes_dict.salt)

        palin_private_key = AES(work_key, cipher_bytes_dict.iv). \
            decrypt(cipher_bytes_dict.cipher, cipher_bytes_dict.gcm_tag)

        return palin_private_key
