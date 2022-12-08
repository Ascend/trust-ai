# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
from gevent import pywsgi
from main.app import app, register_api, init_logger
from config import RUN_LOG, LOG_INFO


if __name__ == "__main__":
    register_api()
    init_logger()
    RUN_LOG.log(LOG_INFO, "Start user-manager service success.")
    server = pywsgi.WSGIServer(("0.0.0.0", 10001), app)
    server.serve_forever()
