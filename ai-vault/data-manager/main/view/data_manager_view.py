# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import os
import json
import time
import shutil
import signal
import zipfile
import socket
from hashlib import sha256
from os.path import getsize, join

import psutil
from flask import Blueprint, views, request, jsonify, send_from_directory

from cfg import status_code
from cfg.config import LOG_INFO, LOG_ERROR, RUN_LOG, AIVAULT_EXPORT_DATA_FILE, COMMON_DIR, HOME_PATH, MAX_DATA_SIZE, \
     RESTART_FLAG, IMPORT_DIR, BACKUP_FLAG, KEY_DATA_WHITE_LIST, INFO_FILE_SIZE, BACKUP_DIR
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
    def format_msg(level, op_name, uid, code, msg=None):
        log_msg = f"[userid: {uid}] [op_name: {op_name}]: {ERROR_MSG_MAP[code]}."
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

    @staticmethod
    def get_zip_file_size(file_path):
        if isinstance(file_path, zipfile.ZipFile):
            file_sizes = (inner_file.file_size for inner_file in file_path.infolist())
            return sum(file_sizes)
        with zipfile.ZipFile(file_path, 'r') as zipf:
            file_sizes = (inner_file.file_size for inner_file in zipf.infolist())
            return sum(file_sizes)

    @staticmethod
    def make_flag_file():
        open(BACKUP_FLAG, "wb").close()

    @staticmethod
    def remove(file_or_dir_path):
        if not os.path.exists(file_or_dir_path):
            return
        if os.path.isfile(file_or_dir_path):
            os.remove(file_or_dir_path)
        if os.path.isdir(file_or_dir_path):
            shutil.rmtree(file_or_dir_path, ignore_errors=True)

    @staticmethod
    def calc_sha256(file_path):
        if not os.path.isfile(file_path):
            raise OSError(f"invalid file path: {file_path}")
        sha256_obj = sha256()
        with open(file_path, 'rb') as file:
            sha256_obj.update(file.read(MAX_DATA_SIZE))
            return sha256_obj.hexdigest()

    @staticmethod
    def get_backup_dir(key_word='dbBackup'):
        backup_dir = ''
        res = os.popen(f"ps -ef |grep '{key_word}'").read()
        if 'ai-vault' not in res:
            return backup_dir
        tmp = [i.strip() for i in res.split("\n")[0].split(" ") if i.strip()]
        for i, v in enumerate(tmp):
            if key_word not in v:
                continue
            if '=' not in v:
                backup_dir = tmp[i + 1]
                break
            backup_dir = i.split("=")[-1]
            break
        return backup_dir

    @staticmethod
    def is_ai_vault_alive():
        res = os.popen(f"ps -ef |grep '/home/AiVault/.ai-vault/ai-vault'").read()
        tmp = [i.strip() for i in res.split("\n")[0].split(" ") if i.strip()]
        if 'run' in tmp and '-mgmtPort' in tmp:
            return True
        return False


class ImportDataView(BaseView):
    """
    导入ai-vault数据
    """
    _op_name = "import data"

    def post(self):
        db_backup_dir = self.get_backup_dir()
        cert_backup_dir = self.get_backup_dir('certBackup')
        try:
            file = request.files.get("file")
            if not file.filename.endswith(".zip"):
                RUN_LOG.log(*self.err_msg(IMPORT_ERROR, "not upload zip file"))
                return self.https_ret(PARAM_ERROR)
            zip_file = zipfile.ZipFile(file)
            if self.get_zip_file_size(zip_file) > MAX_DATA_SIZE:
                RUN_LOG.log(*self.err_msg(IMPORT_ERROR, f"the extracted size of the zip file exceed {MAX_DATA_SIZE >> 20} MB."))
                return self.https_ret(status_code.SIZE_ERROR)
            self._file_check(zip_file)
            zip_file.close()
            self.make_flag_file()
            # stop ai-vault
            self.stop_aivault()
            # backup now data
            self._backup_rollback(db_backup_dir=db_backup_dir, cert_backup_dir=cert_backup_dir)
            # copy new data
            self._copy_key_data(COMMON_DIR, IMPORT_DIR, True, db_backup_dir, cert_backup_dir)
            RUN_LOG.log(*self.info_msg("copy new data successfully"))
            # start aivault
            os.system("/usr/local/openresty/nginx/sbin/nginx -p /home/AiVault/.ai-vault/nginx/ -s reload")
            self._start_aivault(db_backup_dir, cert_backup_dir)
            RUN_LOG.log(*self.info_msg("import data successfully"))
            return self.https_ret(SUCCESS)
        except Exception as e:
            RUN_LOG.log(*self.err_msg(IMPORT_ERROR, e))
            self._backup_rollback(True, db_backup_dir=db_backup_dir, cert_backup_dir=cert_backup_dir)
            return self.https_ret(status_code.IMPORT_ERROR)
        finally:
            self.remove(RESTART_FLAG)
            self.remove(IMPORT_DIR)
            self.remove(BACKUP_FLAG)
            self.remove(BACKUP_DIR)

    def stop_aivault(self):
        pids = psutil.pids()
        RUN_LOG.log(*self.info_msg("start to kill ai-vault"))
        for pid in pids:
            p = psutil.Process(pid)
            process_name = p.name()
            if 'ai-vault' == process_name:
                os.kill(pid, signal.SIGTERM)
                RUN_LOG.log(*self.info_msg("kill ai-vault successfully"))
                os.system(f"touch {RESTART_FLAG}")
                return

    @staticmethod
    def _get_docker_ip():
        return socket.gethostbyname(socket.gethostname())

    def _file_check(self, zip_file):
        invalid_file = "invalid data file"
        for names in zip_file.namelist():
            if names not in KEY_DATA_WHITE_LIST:
                raise ValueError(invalid_file)
            zip_file.extract(names, IMPORT_DIR)
        info_file = os.path.join(IMPORT_DIR, 'info.json')
        if not os.path.exists(info_file):
            raise ValueError("missing info.json in data file")
        with open(info_file, 'rb') as file:
            try:
                file_infos = json.loads(file.read(INFO_FILE_SIZE))
            except json.JSONDecodeError as exc:
                raise ValueError(invalid_file) from exc
        for file_info in file_infos:
            path = os.path.join(IMPORT_DIR, file_info.get("path", ""))
            sha256_value = file_info.get("sha256", "")
            if not os.path.exists(path) or not sha256_value:
                raise ValueError(invalid_file)
            if not os.path.exists(path) or self.calc_sha256(path) != sha256_value:
                raise ValueError(invalid_file)

    def _backup_rollback(self, rollback=False, db_backup_dir='', cert_backup_dir=''):
        if rollback and not os.path.exists(BACKUP_DIR):
            return
        self._copy_key_data(rollback=rollback, db_backup_dir=db_backup_dir, cert_backup_dir=cert_backup_dir)
        if rollback:
            RUN_LOG.log(*self.info_msg("rollback the key data of ai-vault successfully"))
            self._start_aivault(db_backup_dir, cert_backup_dir)
            return
        RUN_LOG.log(*self.info_msg("backup the key data of ai-vault successfully"))

    def _copy_key_data(self, src_dir=COMMON_DIR, dst_dir=BACKUP_DIR, rollback=False, db_backup_dir='', cert_backup_dir=''):
        for backup_file in KEY_DATA_WHITE_LIST:
            if backup_file == 'info.json':
                continue
            src = os.path.join(src_dir, backup_file)
            dst = os.path.join(dst_dir, backup_file)
            if db_backup_dir and 'ai-vault_backup.db' in backup_file:
                relpath = os.path.relpath(backup_file, "backup")
                src = os.path.join(db_backup_dir, relpath)
            if cert_backup_dir and "backup/cert" in backup_file:
                relpath = os.path.relpath(backup_file, "backup")
                src = os.path.join(cert_backup_dir, relpath)
            if rollback:
                src, dst = dst, src
            if not os.path.exists(src):
                raise OSError(f"{src} file not exist.")
            os.makedirs(os.path.dirname(dst), 0o0700, exist_ok=True)
            shutil.copy2(src, dst)

    def _start_aivault(self, db_backup_dir='', cert_backup_dir=''):
        if self.is_ai_vault_alive():
            return
        ip = self._get_docker_ip()
        if not ip or not ip.startswith("172"):
            raise Exception("get docker ip failed")
        if db_backup_dir:
            db_backup_dir = f'-dbBackup {db_backup_dir}'
        if cert_backup_dir:
            cert_backup_dir = f'-certBackup {cert_backup_dir}'
        cmd = f"/home/AiVault/.ai-vault/ai-vault run -ip {ip} -mgmtPort 5000 -servicePort 5001 {db_backup_dir} {cert_backup_dir} & "
        os.system(cmd)
        time.sleep(1)
        if not self.is_ai_vault_alive():
            raise Exception("start ai-vault failed")
        RUN_LOG.log(*self.info_msg("start ai-vault successfully"))


class ExportDataView(BaseView):
    """
    导出ai-vault数据
    """
    _op_name = "export data"

    def get(self):
        try:
            self.make_flag_file()
            self.remove(AIVAULT_EXPORT_DATA_FILE)
            self._zip_file(COMMON_DIR)
            if self.get_zip_file_size(AIVAULT_EXPORT_DATA_FILE) > MAX_DATA_SIZE:
                RUN_LOG.log(*self.err_msg(IMPORT_ERROR, f"the extracted size of the zip file exceed {MAX_DATA_SIZE >> 20} MB."))
                return self.https_ret(status_code.SIZE_ERROR)
            RUN_LOG.log(*self.info_msg("export the key data of aivault successfully"))
            return send_from_directory(directory=HOME_PATH, path="aivault.zip"), 200
        except Exception as e:
            RUN_LOG.log(*self.err_msg(EXPORT_ERROR, e))
            return self.https_ret(status_code.EXPORT_ERROR)
        finally:
            self.remove(AIVAULT_EXPORT_DATA_FILE)
            self.remove(BACKUP_FLAG)

    def _zip_file(self, src_dir):
        """
        压缩工作目录下所有文件
        """
        try:
            zip_file = zipfile.ZipFile(AIVAULT_EXPORT_DATA_FILE, 'w', zipfile.ZIP_DEFLATED)
            file_info = []
            db_backup_dir = self.get_backup_dir()
            cert_backup_dir = self.get_backup_dir('certBackup')
            for backup_file in KEY_DATA_WHITE_LIST:
                if backup_file == 'info.json':
                    continue
                file_path = os.path.join(src_dir, backup_file)
                if db_backup_dir and 'ai-vault_backup.db' in backup_file:
                    file_path = os.path.join(db_backup_dir, 'ai-vault_backup.db')
                if cert_backup_dir and "backup/cert" in backup_file:
                    file_path = os.path.join(cert_backup_dir, os.path.relpath(backup_file, 'backup'))
                zip_file.write(file_path, backup_file)
                file_info.append({
                    "file_name": os.path.basename(backup_file),
                    "path": backup_file,
                    "sha256": self.calc_sha256(file_path)})
            zip_file.writestr("info.json", json.dumps(file_info, indent=4))
        except Exception as e:
            raise e
        finally:
            zip_file.close()


class DataSizeView(BaseView):
    """
    获取数据大小
    """
    _op_name = "get data size"

    def get(self):
        return self.https_ret(status_code.SUCCESS, data={"size": self.get_size()})

    @staticmethod
    def get_size():
        size = 0
        for root, _, files in os.walk(COMMON_DIR):
            size += sum([getsize(join(root, name)) for name in files])
        return size


import_data = ImportDataView.as_view("import")
export_data = ExportDataView.as_view("export")
get_data_size = DataSizeView.as_view("size")


data_manager.add_url_rule("/import",
                          view_func=import_data,
                          methods=("POST",))
data_manager.add_url_rule("/export",
                          view_func=export_data,
                          methods=("GET",))
data_manager.add_url_rule("/size",
                          view_func=get_data_size,
                          methods=("GET",))
