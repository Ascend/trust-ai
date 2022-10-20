# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import re
import os
import binascii
import hashlib

from flask import jsonify

from utils.status_code import ERROR_MSG_MAP
from config import SALT_LEN, KEY_LEN, Iteration_Count


_lower_character_reg = r'[a-z]{1,}'
_upper_character_reg = r'[A-Z]{1,}'
_number_reg = r'[0-9]{1,}'
_special_character_reg = r'[!"#$%&\'()*+,-./:;<=>?@\[\]^_~{}|\\]{1,}'

_passwd_complexity = [_lower_character_reg, _upper_character_reg, _number_reg, _special_character_reg]
_passwd_reg = r'^[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@\[\]^_~{}|\\]{8,20}$'

_name_reg = r'^[a-zA-Z]{1}[a-zA-Z0-9_-]{0,31}$'


def pbkdf2hash(password, salt=None, salt_len=SALT_LEN, key_len=KEY_LEN, iteration=Iteration_Count):
    if isinstance(password, str):
        password = password.encode()
    if isinstance(salt, str):
        salt = binascii.a2b_hex(salt.encode())
    if salt is None:
        salt = os.urandom(salt_len)
    encrypt_password = hashlib.pbkdf2_hmac("sha256", password, salt, iteration, key_len)
    hex_en_passwd_str = binascii.b2a_hex(encrypt_password).decode()
    hex_salt_str = binascii.b2a_hex(salt).decode()
    return hex_en_passwd_str, hex_salt_str


def https_ret(code, data=None, extend_msg=None):
    err_msg = ERROR_MSG_MAP.get(code)
    msg = '%s. %s'.format(err_msg, extend_msg) if extend_msg is not None else err_msg
    return jsonify({
        "status": code,
        "msg": msg,
        "data": data
    })


def format_msg(level, op_name, uid, status_code, msg=None):
    log_msg = f"[userid: {uid}] [op_name: {op_name}]: {ERROR_MSG_MAP[status_code]}."
    if msg:
        log_msg = "{} {}.".format(log_msg, msg)
    return level, log_msg


def passwd_check(password):
    if re.match(_passwd_reg, password) is None:
        return False
    pwd_complex = 0
    for reg in _passwd_complexity:
        if re.search(reg, password) is not None:
            pwd_complex += 1
    if pwd_complex < 2:
        return False
    return True


def name_check(user_name):
    if re.match(_name_reg, user_name) is None:
        return False
    return True
