# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import logging.config as log_conf

import click
from flask import Flask

from cfg.config import LOG_PATH, LOGGING_CONFIG, CERT_PATH, CRT_FILE, KEY_FILE, RUN_LOG_FILE
from main.view.data_manager_view import data_manager

app = Flask(__name__)


def register_api():
    app.register_blueprint(data_manager, url_prefix="/datamanager/v1")


def init_logger():
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH, mode=0o700)
    log_conf.dictConfig(LOGGING_CONFIG)
    os.chmod(RUN_LOG_FILE, 0o600)


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
    register_api()
    init_logger()
    certs_flag = init_certs()
    return certs_flag


@app.teardown_request
def teardown_request(exception):
    pass
