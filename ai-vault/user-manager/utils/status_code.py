# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.

# success
SUCCESS = "00000000"
# parameter error
PARAM_ERROR = "00002000"
# request error
REQUEST_ERROR = "21000001"
# user name not exit
USER_NOT_EXIST_ERROR = "21000002"
# user name exits
USER_EXIST_ERROR = "21000003"
# password error
PASSWD_ERROR = "21000004"
# password error
PASSWD_NOT_SAME = "21000005"
# max user num error
MAX_USER_ERROR = "21000006"
# permission error
PERMISSION_ERROR = "21000007"
# admin delete
ADMIN_DEL_FORBIDDEN = "21000008"
# exist in-use MKs
MK_EXIST = "21000009"

ERROR_MSG_MAP = {
    SUCCESS: "Success Operation",
    PARAM_ERROR: "Parameter Error",
    REQUEST_ERROR: "Request error to other url",
    USER_NOT_EXIST_ERROR: "User does not exist",
    USER_EXIST_ERROR: "User already exists",
    PASSWD_ERROR: "Password Error",
    PASSWD_NOT_SAME: "The password entered twice is inconsistent",
    PERMISSION_ERROR: "User is not allowed to do this operation",
    ADMIN_DEL_FORBIDDEN: "Cannot delete an administrator account",
    MK_EXIST: "User has in-use MKs",
    MAX_USER_ERROR: "The maximum number of users exceeding the limit(500)"
}
