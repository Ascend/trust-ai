# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import logging


WORK_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_PATH = os.path.join(WORK_DIR, "log")
RUN_LOG_FILE = os.path.join(LOG_PATH, "cert_manager_run.log")
DEC_COMMAND = "./../../ai-whitebox dec"
LOG_MAX_SIZE = 10 * 1024 * 1024
LOG_MAX_BACKUP_COUNT = 10
LOG_INFO = 20
LOG_WARN = 30
LOG_ERROR = 40

SALT_LEN = 16
KEY_LEN = 16
Iteration_Count = 10000

COMMON_DIR = os.path.expanduser('~/.ai-vault')
CA_PEM = os.path.join(COMMON_DIR, "ca.pem")
CA_KEY = os.path.join(COMMON_DIR, "ca.key")
TMP_DIR = os.path.join(COMMON_DIR, "tmp")

CERT_PATH = os.path.join(COMMON_DIR, "cert")
CRT_FILE = os.path.join(CERT_PATH, "server.pem")
KEY_FILE = os.path.join(CERT_PATH, "server.key")

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

