# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
from flask import Flask
from main.view.cert_manager_view import cert_manager
from config import TMP_DIR

app = Flask(__name__)


def register_api():
    app.register_blueprint(cert_manager, url_prefix="/usermanager/v1")
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)


@app.teardown_appcontext
def teardown_request(exception):
    pass
