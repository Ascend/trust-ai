# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
from gevent import pywsgi

from main.app import app, init_app
from config import CRT_FILE, KEY_FILE

if __name__ == "__main__":
    if init_app():
        server = pywsgi.WSGIServer(("0.0.0.0", 8084), app, keyfile=KEY_FILE, certfile=CRT_FILE, log=None)
        server.serve_forever()
