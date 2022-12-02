# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
from gevent import pywsgi
from main.app import app, register_api

if __name__ == "__main__":
    register_api()
    server = pywsgi.WSGIServer(("0.0.0.0", 10001), app)
    server.serve_forever()
