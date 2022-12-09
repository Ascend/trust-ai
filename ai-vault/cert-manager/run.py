# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
from gevent import pywsgi
from main.app import app, init_app
from config import CRT_FILE, KEY_FILE, RUN_LOG, LOG_INFO


if __name__ == "__main__":
    if init_app():
        RUN_LOG.log(LOG_INFO, "Start user-manager service success.")
        server = pywsgi.WSGIServer(("0.0.0.0", 10001), app, keyfile=KEY_FILE, certfile=CRT_FILE, log=None)
        server.serve_forever()
