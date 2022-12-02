# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import json
import os.path
import random
import time
import zipfile
import OpenSSL
import OpenSSL.crypto

from flask import Blueprint, views, request, Response
from utils.ssl_key import SSLKey
from config import CA_KEY, CA_PEM, TMP_DIR

cert_manager = Blueprint("cert_manager", __name__)

with open(CA_KEY, "rb") as f:
    KEY_BYTES = f.read()
with open(CA_PEM, "rb") as f:
    CRT_BYTES = f.read()
PASSWD = "qwerty"


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
    pri_key.generate_key(OpenSSL.crypto.TYPE_RSA, int(data.get("KeyLen", "3072")))
    pri_key.to_cryptography_key()

    req = OpenSSL.crypto.X509Req()
    req.get_subject().commonName = data.get("CommonName")
    req.get_subject().countryName = data.get("CountryName")
    req.get_subject().stateOrProvinceName = data.get("StateOrProvinceName")
    req.get_subject().localityName = data.get("LocalityName")
    req.get_subject().organizationName = data.get("OrganizationName")
    req.get_subject().organizationalUnitName = data.get("OrganizationalUnitName")
    req.get_subject().emailAddress = data.get("EmailAddress")

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

    @staticmethod
    def get_request_json():
        json_data = None
        try:
            data = request.get_data()
            json_data = json.loads(data)
        except json.JSONDecodeError:
            err_msg = "Get request json data error"
            # RUN_LOG.log(*format_msg(LOG_ERROR, self._op_name, self.uid, status_code.PARAM_ERROR, err_msg))
            json_data = {}
        finally:
            return json_data


class GenPriKeyAndCrtView(BaseView):
    """
    Generate private key and CSR
    """
    _op_name = "GenKeyAndCrt"

    def __int__(self, *args, **kwargs):
        super().__int__(*args, **kwargs)
        self.ca_crt = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, CRT_BYTES)
        self.data = {}

    def post(self):
        self.data = self.get_request_json()

        zip_path = self.zip_file()
        with open(zip_path, "rb") as zip_fp:
            zip_data = zip_fp.read()
        os.remove(zip_path)

        res = Response(zip_data, content_type="application/octet-stream")
        res.headers["Content-disposition"] = f'attachment; filename=key_cert.zip'
        return res

    def zip_file(self):
        pri_key, csr = gen_prikey_and_csr(self.data)
        ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, KEY_BYTES, PASSWD.encode())
        common_name, cert = sign_cert(self.ca_crt, ca_key, csr)
        file_name = str(hash(common_name)) + str(hash(time.time())) + str(hash(random.randint(0, 100000))) + ".zip"
        zip_path = os.path.join(TMP_DIR, file_name)
        zip_content = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        zip_content.writestr(f"{common_name}.key", pri_key)
        zip_content.writestr(f"f{common_name}.pem", cert)
        zip_content.close()
        return zip_path


class SignCertView(BaseView):
    """
    Sign cert for flask
    """
    _op_name = "SignCert"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ca_crt = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, CRT_BYTES)

    def post(self):
        csr = request.files["CSR"].read()
        ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, KEY_BYTES, PASSWD.encode())

        common_name, crt = sign_cert(self.ca_crt, ca_key, csr)
        res = Response(crt, content_type="application/octet-stream")
        res.headers["Content-disposition"] = f'attachment; filename={common_name}.pem'

        return res


class GetCFSCertView(BaseView):
    """
    get CFS Certificate
    """
    _op_name = "GetCFS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {}
        self.ssl_aes = SSLKey()
        self.ca_crt = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, CRT_BYTES)

    def post(self):
        self.data = self.get_request_json()
        pri_key, csr = gen_prikey_and_csr(self.data)
        ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, KEY_BYTES, PASSWD.encode())
        common_name, cert = sign_cert(self.ca_crt, ca_key, csr)
        cipher_pri_key = self.ssl_aes.encrypt_pri_key(pri_key, self.data.get("CfsPassword"))

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
        res.headers["Content-disposition"] = f'attachment; filename=cfs.zip'
        return res


class GetCACertView(BaseView):
    """
    Get CA certificate
    """
    _op_name = "GetCA"

    @staticmethod
    def get():
        res = Response(CRT_BYTES, content_type="application/octet-stream")
        res.headers["Content-disposition"] = 'attachment; filename=ca.pem'
        return res


key_crt_v = GenPriKeyAndCrtView.as_view("get_key_crt")
sign_v = SignCertView.as_view("sign_cert")
ca_v = GetCACertView.as_view("get_ca")
cfs_v = GetCFSCertView.as_view("get_cfs")

cert_manager.add_url_rule("/key",
                          endpoint="csr",
                          view_func=key_crt_v,
                          methods=("POST",))
cert_manager.add_url_rule("/sign",
                          endpoint="sign",
                          view_func=sign_v,
                          methods=("POST",))
cert_manager.add_url_rule("/ca",
                          endpoint="ca",
                          view_func=ca_v,
                          methods=("GET",))
cert_manager.add_url_rule("/cfs",
                          endpoint="cfs",
                          view_func=cfs_v,
                          methods=("POST",))
