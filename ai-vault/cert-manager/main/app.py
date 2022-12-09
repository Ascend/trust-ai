# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import click
from flask import Flask
import logging.config as log_conf
from main.view.cert_manager_view import cert_manager
from config import TMP_DIR, LOG_PATH, RUN_LOG_FILE, LOGGING_CONFIG, CERT_PATH, CRT_FILE, KEY_FILE

app = Flask(__name__)


def register_api():
    app.register_blueprint(cert_manager, url_prefix="/certmanager/v1")
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)


def init_logger():
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH, mode=0o750)
    log_conf.dictConfig(LOGGING_CONFIG)
    os.chmod(RUN_LOG_FILE, 0o640)


def init_certs():
    if not os.path.exists(CERT_PATH):
        os.makedirs(CERT_PATH)
        click.secho("Please place the cert file in the cert directory.")
        return False
    if not os.path.exists(CRT_FILE):
        click.secho("Please place the crt file in the cert directory.")
        return False
    if not os.path.exists(KEY_FILE):
        click.secho("Please place the key file in the cert directory.")
        return False
    return True


def init_app():
    init_logger()
    certs_flag = init_certs()
    register_api()
    return certs_flag


@app.teardown_appcontext
def teardown_request(exception):
    pass
