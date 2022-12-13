# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import logging


WORK_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_PATH = os.path.join(os.path.dirname(WORK_DIR), "log")
RESTART_FLAG = os.path.join(os.path.dirname(WORK_DIR), "restart_flag")
BACKUP_FLAG = os.path.join(os.path.dirname(WORK_DIR), "backup_flag")
RUN_LOG_FILE = os.path.join(LOG_PATH, "data_manager_run.log")
LOG_MAX_SIZE = 10 * 1024 * 1024
LOG_MAX_BACKUP_COUNT = 10
LOG_INFO = 20
LOG_WARN = 30
LOG_ERROR = 40
MAX_DATA_SIZE = 50 * 1024 * 1024
INFO_FILE_SIZE = 1024 * 1024

HOME_PATH = os.path.expanduser('~')
AIVAULT_EXPORT_DATA_FILE = os.path.join(HOME_PATH, 'aivault.zip')
COMMON_DIR = os.path.join(HOME_PATH, '.ai-vault')
IMPORT_DIR = os.path.join(HOME_PATH, '.ai-vault_bak')
BACKUP_DIR = os.path.join(HOME_PATH, '.ai-vault_backup')
CERT_PATH = os.path.join(COMMON_DIR, "cert")
CRT_FILE = os.path.join(CERT_PATH, "server.pem")
KEY_FILE = os.path.join(CERT_PATH, "server.key")
KEY_DATA_WHITE_LIST = (
    "info.json",
    "ai-vault.db",
    "backup/ai-vault_backup.db",
    "backup/cert/server.key",
    "backup/cert/server.pem",
    "backup/cert/mgmt/ca.pem",
    "backup/cert/mgmt/hmac.json",
    "backup/cert/mgmt/mgmt.csr",
    "backup/cert/mgmt/mgmt.key",
    "backup/cert/mgmt/mgmt.pem",
    "backup/cert/svc/ca.pem",
    "backup/cert/svc/hmac.json",
    "backup/cert/svc/svc.csr",
    "backup/cert/svc/svc.key",
    "backup/cert/svc/svc.pem",
    "ca.key",
    "ca.pem",
    "cert/server.key",
    "cert/server.pem",
    "cert/mgmt/ca.pem",
    "cert/mgmt/hmac.json",
    "cert/mgmt/mgmt.csr",
    "cert/mgmt/mgmt.key",
    "cert/mgmt/mgmt.pem",
    "cert/svc/ca.pem",
    "cert/svc/hmac.json",
    "cert/svc/svc.csr",
    "cert/svc/svc.key",
    "cert/svc/svc.pem",
    "encrypted_password",
    "ksf/0/backup.dat",
    "ksf/0/master.dat",
    "user-manager/user_manager.sqlite"
)
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
