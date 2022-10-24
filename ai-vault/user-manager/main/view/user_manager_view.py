# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import json

from functools import wraps
from flask import Blueprint, views, request

from utils import status_code
from utils.sqlite_operation import User
from utils.tools import name_check, https_ret, passwd_check, format_msg
from config import Admin_User, CRT_FILE, KEY_FILE, GET_TIMEOUT, LOG_INFO, \
    LOG_ERROR, AUTH_MAP, INSTALL_PARAM, MAX_URL_LEN, RUN_LOG

user_manager = Blueprint("user_manager", __name__)


def user_exist_require(func):
    @wraps(func)
    def inner(*args, **kwargs):
        uid = request.headers.get("UserID")
        if uid is None:
            return https_ret(status_code.USER_NOT_EXIST_ERROR)
        user = User.query.filter_by(user_id=int(uid)).first()
        if user is None:
            return https_ret(status_code.USER_NOT_EXIST_ERROR)
        else:
            return func(*args, **kwargs)
    return inner


class BaseView(views.MethodView):
    """
    基础视图
    """
    _op_name = "Base operation"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = int(request.headers.get("UserID")) if request.headers.get("UserID") else None

    def get_request_json(self):
        json_data = None
        try:
            data = request.get_data()
            json_data = json.loads(data)
        except json.JSONDecodeError:
            err_msg = "Get request json data error"
            RUN_LOG.log(*format_msg(LOG_ERROR, self._op_name, self.uid, status_code.PARAM_ERROR, err_msg))
            json_data = {}
        finally:
            return json_data

    def err_msg(self, status, msg=None):
        return format_msg(LOG_ERROR, self._op_name, self.uid, status, msg)

    def info_msg(self, msg=None):
        return format_msg(LOG_INFO, self._op_name, self.uid, status_code.SUCCESS, msg)

    def check_err_msg(self, key_name):
        err_msg = f"Param {key_name} check failed"
        return self.err_msg(status_code.PARAM_ERROR, err_msg)

    def parameter_check(self, parameters):
        for key, value in parameters.items():
            if len(parameters) == 0:
                RUN_LOG.log(*self.err_msg(status_code.PARAM_ERROR, "Parameter is null"))
                return False
            if key == "UserName" and not name_check(value):
                RUN_LOG.log(*self.check_err_msg(key))
                return False
            if key in ["Password", "PasswordConfirm", "NewPassword", "NewPasswordConfirm"] and not passwd_check(value):
                RUN_LOG.log(*self.check_err_msg(key))
                return False
            if key == "SortMode" and value not in ["desc", "asc"]:
                RUN_LOG.log(*self.check_err_msg(key))
                return False
            if key == "SortBy" and value not in ["UserID", "UserName", "CreateTime", "LastLoginTime"]:
                RUN_LOG.log(*self.check_err_msg(key))
                return False
        return True

    def get_with_log(self, param_dict, key):
        data = param_dict.get(key)
        if data is None:
            RUN_LOG.log(*self.check_err_msg(key))
        return data


class LoginUserView(BaseView):
    """
    用户登录
    """
    _op_name = "Login"

    def post(self):
        data = self.get_request_json()
        if not self.parameter_check(data):
            return https_ret(status_code.PARAM_ERROR)
        user_name = self.get_with_log(data, "UserName")
        passwd = self.get_with_log(data, "Password")
        if user_name is None or passwd is None:
            return https_ret(status_code.PARAM_ERROR)
        status, user_data = User.user_login(user_name, passwd)
        if status == status_code.SUCCESS:
            RUN_LOG.log(*self.info_msg(f"User {user_name} login success"))
            return https_ret(status, user_data)
        RUN_LOG.log(*self.err_msg(status, f"User {user_name} login failed"))
        return https_ret(status)


class AddUserView(BaseView):
    """
    管理员添加用户
    """
    _op_name = "Add User"

    def post(self):
        data = self.get_request_json()
        if not self.parameter_check(data):
            return https_ret(status_code.PARAM_ERROR)
        user_name = self.get_with_log(data, "UserName")
        passwd = self.get_with_log(data, "Password")
        passwd_confirm = self.get_with_log(data, "PasswordConfirm")
        if user_name is None or passwd is None or passwd_confirm is None:
            return https_ret(status_code.PARAM_ERROR)
        if passwd != passwd_confirm:
            RUN_LOG.log(*self.err_msg(status_code.PASSWD_NOT_SAME))
            return https_ret(status_code.PASSWD_NOT_SAME)
        status = User.add_user(user_name, passwd)
        if status == status_code.SUCCESS:
            RUN_LOG.log(*self.info_msg(f"Add user {user_name} success"))
            return https_ret(status, user_name)
        RUN_LOG.log(*self.err_msg(status))
        return https_ret(status)


class DelUserView(BaseView):
    """
    管理员删除用户
    """
    _op_name = "Del User"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._query_url = self._get_query_url()

    @staticmethod
    def _get_query_url():
        if INSTALL_PARAM.get("AIVAULT_INTERFACE") is None:
            return "/"
        return INSTALL_PARAM.get("AIVAULT_INTERFACE")

    def delete(self, user_name):
        if not name_check(user_name):
            RUN_LOG.log(*self.check_err_msg("UserName"))
            return https_ret(status_code.PARAM_ERROR)
        if user_name == "admin":
            RUN_LOG.log(*self.err_msg(status_code.ADMIN_DEL_FORBIDDEN))
            return status_code.ADMIN_DEL_FORBIDDEN
        keys_check, status = self.check_key_status(user_name)
        if not keys_check:
            return https_ret(status)
        status = User.delete_user(user_name)
        if status == status_code.SUCCESS:
            RUN_LOG.log(*self.info_msg(f"Del user {user_name} success"))
            return https_ret(status)
        RUN_LOG.log(*self.err_msg(status))
        return https_ret(status)

    def check_key_status(self, user_name):
        import requests
        import urllib3
        from urllib.parse import urljoin
        urllib3.disable_warnings()
        get_ok, user = User.get_user_by_name(user_name)
        if not get_ok:
            return False, user

        query_mk = urljoin(self._query_url, "AIVAULT/v1/queryMK")
        try:
            mk_res = requests.request(method="GET", url=query_mk, headers={"DomainID": str(user.user_id)},
                                      verify=False, cert=(CRT_FILE, KEY_FILE), timeout=GET_TIMEOUT)
            if mk_res.status_code != 200:
                RUN_LOG.log(*self.err_msg(status_code.REQUEST_ERROR, "Can not get data from ai-vault"))
                return False, status_code.REQUEST_ERROR
            if json.loads(mk_res.content)["data"]["totalCount"] != 0:
                RUN_LOG.log(*self.err_msg(status_code.MK_EXIST, f"Can not del {user_name}"))
                return False, status_code.MK_EXIST
        except requests.exceptions.ConnectionError:
            RUN_LOG.log(*self.err_msg(status_code.REQUEST_ERROR, "Can not connect to ai-vault"))
            return False, status_code.REQUEST_ERROR
        except json.JSONDecodeError:
            RUN_LOG.log(*self.err_msg(status_code.REQUEST_ERROR, "Data get from ai-vault is not json data"))
            return False, status_code.REQUEST_ERROR
        else:
            return True, None


class ResetPasswordView(BaseView):
    """
    管理员重置用户
    """
    _op_name = "ResetPWD"

    def post(self):
        data = self.get_request_json()
        if not self.parameter_check(data):
            return https_ret(status_code.PARAM_ERROR)
        user_name = self.get_with_log(data, "UserName")
        new_passwd = self.get_with_log(data, "NewPassword")
        if user_name is None or new_passwd is None:
            return https_ret(status_code.PARAM_ERROR)
        if new_passwd != self.get_with_log(data, "NewPasswordConfirm"):
            RUN_LOG.log(*self.err_msg(status_code.PASSWD_NOT_SAME))
            return https_ret(status_code.PASSWD_NOT_SAME)
        status = User.reset_password(user_name, new_passwd)
        if status == status_code.SUCCESS:
            RUN_LOG.log(*self.info_msg("Update Password Success"))
            return https_ret(status)
        RUN_LOG.log(*self.err_msg(status))
        return https_ret(status)


class QueryUserView(BaseView):
    """
    查询用户，支持管理员与普通用户
    """
    decorators = [user_exist_require]

    _op_name = "Query User"

    def get(self):
        data = request.args
        if not self.parameter_check(data):
            return https_ret(status_code.PARAM_ERROR)
        kwargs = {
            "current_page": int(data.get("CurrentPage")) if data.get("CurrentPage") else None,
            "pagesize": int(data.get("PageSize")) if data.get("PageSize") else None,
            "user_name": data.get("UserName"),
            "sort_by": data.get("SortBy"),
            "sort_mode": data.get("SortMode")
        }
        status, user_data = User.query_user(**kwargs)
        if status == status_code.SUCCESS:
            RUN_LOG.log(*self.info_msg("Query Success"))
            return https_ret(status, data=user_data)
        RUN_LOG.log(*self.err_msg(status))
        return https_ret(status)


class UpdatePasswordView(BaseView):
    """
    用户更新密码
    """
    decorators = [user_exist_require]

    _op_name = "UpdatePWD"

    def post(self):
        data = self.get_request_json()
        if not self.parameter_check(data):
            return https_ret(status_code.PARAM_ERROR)
        passwd = self.get_with_log(data, "Password")
        new_passwd = self.get_with_log(data, "NewPassword")
        if passwd is None or new_passwd is None:
            return https_ret(status_code.PARAM_ERROR)
        if new_passwd != self.get_with_log(data, "NewPasswordConfirm"):
            RUN_LOG.log(*self.err_msg(status_code.PASSWD_NOT_SAME))
            return https_ret(status_code.PASSWD_NOT_SAME)
        status = User.update_password(passwd, new_passwd, self.uid)
        if status == status_code.SUCCESS:
            RUN_LOG.log(*self.info_msg("Update Password Success"))
            return https_ret(status)
        RUN_LOG.log(*self.err_msg(status))
        return https_ret(status)


class AuthenticationView(BaseView):
    """
    用户鉴权
    """
    decorators = [user_exist_require]

    _op_name = "Authentication"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_map = self._check_auth_map()

    @staticmethod
    def _check_auth_map():
        auth_map = AUTH_MAP
        if auth_map.get("Admin_Interface") is None:
            auth_map["Admin_Interface"] = {"admin": {"GET": [], "POST": [], "DELETE": []}}
        if auth_map.get("Normal_Interface") is None:
            auth_map["Normal_Interface"] = {"admin": {"GET": [], "POST": [], "DELETE": []}}
        for func in ["POST", "GET", "DELETE"]:
            if auth_map["Admin_Interface"].get(func) is None:
                auth_map["Admin_Interface"][func] = []
            if auth_map["Normal_Interface"].get(func) is None:
                auth_map["Normal_Interface"][func] = []
        return auth_map

    def post(self):
        data = self.get_request_json()
        func_name = self.get_with_log(data, "FuncName")
        prefix = self.get_with_log(data, "Prefix")
        status, operation = self.check_prefix(func_name, prefix)
        if status == status_code.SUCCESS:
            RUN_LOG.log(*self.info_msg(f"Authentication passed. {operation}"))
            return https_ret(status)
        RUN_LOG.log(*self.err_msg(status))
        return https_ret(status)

    def check_prefix(self, func_name, prefix):
        if prefix is None or func_name not in ["POST", "GET", "DELETE"]:
            return status_code.PERMISSION_ERROR, None
        if len(prefix) > MAX_URL_LEN:
            return status_code.PERMISSION_ERROR, None
        if self.uid == Admin_User:
            for interface in AUTH_MAP["Admin_Interface"][func_name]:
                if prefix.startswith(interface):
                    return status_code.SUCCESS, f"Interface: <{func_name}-{interface}>"
        else:
            for interface in AUTH_MAP["Normal_Interface"][func_name]:
                if prefix.startswith(interface):
                    return status_code.SUCCESS, f"Interface: <{func_name}-{interface}>"
        return status_code.PERMISSION_ERROR, None


liv = LoginUserView.as_view("login")
auv = AddUserView.as_view("add_user")
duv = DelUserView.as_view("del_user")
qv = QueryUserView.as_view("user_list")
upv = UpdatePasswordView.as_view("update_pwd")
rpv = ResetPasswordView.as_view("reset_pwd")
authv = AuthenticationView.as_view("authentication")

user_manager.add_url_rule("/login",
                          endpoint="login",
                          view_func=liv,
                          methods=("POST",))
user_manager.add_url_rule("/user",
                          endpoint="add_user",
                          view_func=auv,
                          methods=("POST",))
user_manager.add_url_rule("/user/<user_name>",
                          endpoint="del_user",
                          view_func=duv,
                          methods=("DELETE",))
user_manager.add_url_rule("/query",
                          endpoint="query",
                          view_func=qv,
                          methods=("GET",))
user_manager.add_url_rule("/password",
                          endpoint="update_pwd",
                          view_func=upv,
                          methods=("POST",))
user_manager.add_url_rule("/reset",
                          endpoint="reset_pwd",
                          view_func=rpv,
                          methods=("POST",))
user_manager.add_url_rule("/auth",
                          endpoint="authentication",
                          view_func=authv,
                          methods=("POST",))
