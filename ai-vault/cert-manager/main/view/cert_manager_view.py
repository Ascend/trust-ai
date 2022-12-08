# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import json
import os.path
import random
import subprocess
import time
import zipfile
import OpenSSL
import OpenSSL.crypto

from config import LOG_INFO, LOG_ERROR, RUN_LOG
from utils.tools import check_param, https_rsp
from utils import status_code
from flask import Blueprint, views, request, Response
from utils.ssl_key import SSLKey
from config import CA_KEY, CA_PEM, TMP_DIR

cert_manager = Blueprint("cert_manager", __name__)


def get_CA_key_cert(key_path, crt_path):
    with open(key_path, "rb") as f:
        key_byte = f.read()
    with open(crt_path, "rb") as f:
        crt_byte = f.read()
    return key_byte, crt_byte


KEY_BYTES, CRT_BYTES = get_CA_key_cert(CA_KEY, CA_PEM)


def get_plain_passwd(command):
    """
    decrypt password by whitebox and get plain password
    """
    output = subprocess.Popen(command, shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    passwd_byte = output.communicate()[0]
    passwd = passwd_byte.decode(encoding="utf-8")
    return passwd


PASSWD = get_plain_passwd("./../cert/ai-whitebox dec")


def sign_cert(ca_crt, ca_key, csr: bytes):
    """
    sign service crt by ca key
    """
    client_csr = OpenSSL.crypto.load_certificate_request(OpenSSL.crypto.FILETYPE_PEM, csr)

    client_subject = client_csr.get_subject()
    common_name = client_subject.commonName
    client_pubkey = client_csr.get_pubkey()
    ca_subject = ca_crt.get_subject()

    client_crt = OpenSSL.crypto.X509()
    client_crt.set_version(2)
    client_crt.set_serial_number(1)
    client_crt.set_subject(client_subject)
    client_crt.set_issuer(ca_subject)
    client_crt.set_pubkey(client_pubkey)
    client_crt.gmtime_adj_notBefore(0)
    client_crt.gmtime_adj_notAfter(180 * 24 * 60 * 60)
    client_crt.sign(ca_key, 'sha256')

    return common_name, OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, client_crt)


def gen_prikey_and_csr(data):
    pri_key = OpenSSL.crypto.PKey()
    pri_key.generate_key(OpenSSL.crypto.TYPE_RSA, 3072)
    pri_key.to_cryptography_key()

    req = OpenSSL.crypto.X509Req()
    if data.get("CommonName"):
        req.get_subject().commonName = data.get("CommonName")
    if data.get("CountryName"):
        req.get_subject().countryName = data.get("CountryName")
    if data.get("StateOrProvinceName"):
        req.get_subject().stateOrProvinceName = data.get("StateOrProvinceName")
    if data.get("LocalityName"):
        req.get_subject().localityName = data.get("LocalityName")
    if data.get("OrganizationName"):
        req.get_subject().organizationName = data.get("OrganizationName")
    if data.get("OrganizationalUnitName"):
        req.get_subject().organizationalUnitName = data.get("OrganizationalUnitName")

    req.set_pubkey(pri_key)
    req.sign(pri_key, 'sha256')

    pri_key_export = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, pri_key)
    csr = OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_PEM, req)

    return pri_key_export, csr


class BaseView(views.MethodView):
    """
    Base View for flask
    """
    _op_name = "Base operation"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = int(request.headers.get("UserID")) if request.headers.get("UserID") else None

    @staticmethod
    def get_request_json():
        json_data = None
        try:
            data = request.get_data()
            json_data = json.loads(data)
        except json.JSONDecodeError:
            err_msg = "Get request json data error"
            RUN_LOG.log(*format_msg(LOG_ERROR, self._op_name, self.uid, status_code.PARAM_ERROR, err_msg))
            json_data = {}
        finally:
            return json_data

    def err_msg(self, status, msg=None):
        return format_msg(LOG_ERROR, self._op_name, self.uid, status, msg)

    def info_msg(self, msg=None):
        return format_msg(LOG_INFO, self._op_name, self.uid, status_code.SUCCESS, msg)


class GetCFSCertView(BaseView):
    """
    get CFS Certificate
    """
    _op_name = "Get CFS Cert"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {}
        self.ssl_aes = SSLKey()
        self.ca_crt = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, CRT_BYTES)

    def post(self):
        self.data = self.get_request_json()
        status = check_param(self.data)
        if status != status_code.SUCCESS:
            RUN_LOG.log(*err_msg(status, "CSR Param Check Failed"))
            return https_rsp(status)

        pri_key, csr = gen_prikey_and_csr(self.data)
        ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, KEY_BYTES, PASSWD.encode())
        common_name, cert = sign_cert(self.ca_crt, ca_key, csr)
        cipher_pri_key, status = self.ssl_aes.encrypt_pri_key(pri_key, self.data.get("CfsPassword"))
        if status != status_code.SUCCESS:
            RUN_LOG.log(*err_msg(status, "Password Check Failed"))
            return https_rsp(status)

        file_name = str(hash(common_name)) + str(hash(time.time())) + str(hash(random.randint(0, 100000))) + ".zip"
        zip_path = os.path.join(TMP_DIR, file_name)
        zip_content = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        zip_content.writestr("cfs.key", cipher_pri_key)
        zip_content.writestr("cfs.pem", cert)
        zip_content.writestr("ca.pem", CRT_BYTES)
        zip_content.close()

        with open(zip_path, "rb") as zip_fp:
            zip_data = zip_fp.read()
        os.remove(zip_path)

        res = Response(zip_data, content_type="application/octet-stream")
        res.headers["Content-disposition"] = f'attachment; filename=cfs_cert.zip'
        RUN_LOG.log(*self.info_msg("Get CFS Cert and Key Success"))

        return res


cfs_v = GetCFSCertView.as_view("get_cfs")

cert_manager.add_url_rule("/getcert",
                          endpoint="getcert",
                          view_func=cfs_v,
                          methods=("POST",))
