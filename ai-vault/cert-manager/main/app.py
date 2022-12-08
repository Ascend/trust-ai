# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
from flask import Flask
import logging.config as log_conf
from main.view.cert_manager_view import cert_manager
from config import TMP_DIR, LOG_PATH, RUN_LOG_FILE, LOGGING_CONFIG

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


@app.teardown_appcontext
def teardown_request(exception):
    pass
