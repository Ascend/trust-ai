# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import json
import logging


def _get_json_data(json_path):
    with open(json_path) as f:
        data = f.read()
        cfg = json.loads(data)
    return cfg


Admin_User = 500
Admin_Role = 1
Normal_Role = 4
SALT_LEN = 16
KEY_LEN = 32
Iteration_Count = 10000
MAX_USER_NUM = 500
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_URL_LEN = 300

WORK_DIR = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(WORK_DIR, "user_manager.sqlite")
SQL_DB = "sqlite:///{db}".format(db=DB_PATH)
LOG_PATH = os.path.join(WORK_DIR, "log")
RUN_LOG_FILE = os.path.join(LOG_PATH, "user_manager_run.log")
LOG_MAX_SIZE = 10 * 1024 * 1024
LOG_MAX_BACKUP_COUNT = 10
LOG_INFO = 20
LOG_WARN = 30
LOG_ERROR = 40

CONF_PATH = os.path.join(WORK_DIR, "configuration")
AUTH_MAP = _get_json_data(os.path.join(CONF_PATH, "authentication.json"))
INSTALL_PARAM = _get_json_data(os.path.join(CONF_PATH, "install_param.json"))

COMMON_DIR = os.path.expanduser('~/.ai-vault')
CERT_PATH = os.path.join(COMMON_DIR, "cert")
CRT_FILE = os.path.join(CERT_PATH, "server.pem")
KEY_FILE = os.path.join(CERT_PATH, "server.key")
GET_TIMEOUT = 60

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detail': {
            'format': '[%(levelname)s] [%(asctime)s] [pid:%(process)d] [%(filename)s:%(lineno)d] %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] > %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },
        'run_file_handler': {
            'level': 'INFO',
            'class': 'utils.log.MyRotatingFileHandler',
            'filename': RUN_LOG_FILE,
            'maxBytes': LOG_MAX_SIZE,
            'backupCount': LOG_MAX_BACKUP_COUNT,
            'formatter': 'detail',
        },
    },
    'loggers': {
        'run': {
            'handlers': ['run_file_handler'],
            'level': 'INFO',
            'propagate': False,
        },
        'console': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

RUN_LOG = logging.getLogger("run")
