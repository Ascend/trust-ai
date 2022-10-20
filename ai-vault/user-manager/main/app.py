# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import logging.config as log_conf

import click
from flask import Flask

from utils.sqlite_operation import db, User
from main.view.user_manager_view import user_manager
from config import LOG_PATH, RUN_LOG_FILE, DB_PATH, LOGGING_CONFIG, CERT_PATH, CRT_FILE, KEY_FILE, INSTALL_PARAM, SQL_DB
app = Flask(__name__)


def register_api():
    app.register_blueprint(user_manager, url_prefix="/usermanager/v1")


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


def init_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = SQL_DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()
        os.chmod(DB_PATH, 0o600)
        admin_flag = User.check_admin(INSTALL_PARAM)
    return admin_flag


def init_app():
    init_logger()
    certs_flag = init_certs()
    db_flag = init_db()
    register_api()
    return certs_flag and db_flag


@app.teardown_request
def teardown_request(exception):
    db.session.remove()
