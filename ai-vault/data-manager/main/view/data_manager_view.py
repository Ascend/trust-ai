# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import signal
import zipfile
import socket

import psutil
from flask import Blueprint, views, request, jsonify, send_from_directory

from cfg import status_code
from cfg.config import LOG_INFO, LOG_ERROR, RUN_LOG, AIVAULT_EXPORT_DATA_FILE, COMMON_DIR, HOME_PATH
from cfg.status_code import ERROR_MSG_MAP, EXPORT_ERROR, IMPORT_ERROR, SUCCESS, PARAM_ERROR

data_manager = Blueprint("data_manager", __name__)


class BaseView(views.MethodView):
    """
    基础视图
    """
    _op_name = "Base operation"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = int(request.headers.get("UserID")) if request.headers.get("UserID") else None

    def err_msg(self, status, msg=None):
        return self.format_msg(LOG_ERROR, self._op_name, self.uid, status, msg)

    def info_msg(self, msg=None):
        return self.format_msg(LOG_INFO, self._op_name, self.uid, status_code.SUCCESS, msg)

    @staticmethod
    def format_msg(level, op_name, uid, status_code, msg=None):
        log_msg = f"[userid: {uid}] [op_name: {op_name}]: {ERROR_MSG_MAP[status_code]}."
        if msg:
            log_msg = "{} {}.".format(log_msg, msg)
        return level, log_msg

    @staticmethod
    def https_ret(code, data=None, extend_msg=None):
        err_msg = ERROR_MSG_MAP.get(code)
        msg = '%s. %s'.format(err_msg, extend_msg) if extend_msg is not None else err_msg
        return jsonify({
            "status": code,
            "msg": msg,
            "data": data
        })


class ImportDataView(BaseView):
    """
    导入ai-vault数据
    """
    _op_name = "import data"

    def post(self):
        try:
            file = request.files.get("file")
            if not file.filename.endswith(".zip"):
                RUN_LOG.log(*self.err_msg(IMPORT_ERROR, "not upload zip file"))
                return self.https_ret(PARAM_ERROR)
            # stop ai-vault
            self.stop_aivault()
            zip_file = zipfile.ZipFile(file)
            for names in zip_file.namelist():
                zip_file.extract(names, COMMON_DIR)
            zip_file.close()
            # start aivault
            self._start_aivault()
            RUN_LOG.log(*self.err_msg(SUCCESS, "import data successful"))
            return self.https_ret(SUCCESS)
        except Exception as e:
            RUN_LOG.log(*self.err_msg(IMPORT_ERROR, e))
            return self.https_ret(status_code.IMPORT_ERROR)

    def stop_aivault(self):
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            process_name = p.name()
            if 'ai-vault' == process_name:
                RUN_LOG.log(*self.info_msg("start kill ai-vault"))
                os.kill(pid, signal.SIGKILL)
                return

    @staticmethod
    def _get_docker_ip():
        return socket.gethostbyname(socket.gethostname())

    def _start_aivault(self):
        ip = self._get_docker_ip()
        if not ip or not ip.startswith("172"):
            raise Exception("get docker ip failed")
        cmd = f"/home/AiVault/.ai-vault/ai-vault run -ip {ip} -mgmtPort 5000 -servicePort 5001 & "
        ret = os.system(cmd)
        if ret:
            RUN_LOG.log(*self.err_msg(IMPORT_ERROR, f"start ai-vault failed, ret({ret})"))
            raise Exception("start ai-vault failed")


class ExportDataView(BaseView):
    """
    导出ai-vault数据
    """
    _op_name = "export data"

    def get(self):
        try:
            if os.path.exists(AIVAULT_EXPORT_DATA_FILE):
                os.remove(AIVAULT_EXPORT_DATA_FILE)
            self.zip_file(COMMON_DIR)
            return send_from_directory(directory=HOME_PATH, path="aivault.zip"), 200
        except Exception as e:
            RUN_LOG.log(*self.err_msg(EXPORT_ERROR, e))
            return self.https_ret(status_code.EXPORT_ERROR)
        finally:
            os.remove(AIVAULT_EXPORT_DATA_FILE)

    @staticmethod
    def zip_file(src_dir):
        """
        压缩工作目录下所有文件
        """
        try:
            z = zipfile.ZipFile(AIVAULT_EXPORT_DATA_FILE, 'w', zipfile.ZIP_DEFLATED)
            for dirpath, dirnames, filenames in os.walk(src_dir):
                fpath = dirpath.replace(src_dir, '')
                fpath = fpath and fpath + os.sep or ''
                for filename in filenames:
                    if filename.endswith(".log"):
                        continue
                    z.write(os.path.join(dirpath, filename), fpath + filename)
        except Exception as e:
            raise e
        finally:
            z.close()


import_data = ImportDataView.as_view("import")
export_data = ExportDataView.as_view("export")


data_manager.add_url_rule("/import",
                          view_func=import_data,
                          methods=("POST",))
data_manager.add_url_rule("/export",
                          view_func=export_data,
                          methods=("GET",))
