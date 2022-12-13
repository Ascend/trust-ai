# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import logging.handlers

from config import LOG_MAX_BACKUP_COUNT


class MyRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self):
        try:
            os.chmod(self.baseFilename, mode=0o440)
        except PermissionError:
            os.chmod(f"{self.baseFilename}.{LOG_MAX_BACKUP_COUNT}", mode=0o640)
        finally:
            logging.handlers.RotatingFileHandler.doRollover(self)
            os.chmod(self.baseFilename, mode=0o640)
