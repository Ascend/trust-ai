# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import datetime

import click
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import SQLAlchemy

from utils import status_code
from utils.tools import pbkdf2hash
from config import RUN_LOG, Admin_User, Admin_Role, Normal_Role, MAX_USER_NUM, DEFAULT_PAGE, \
    DEFAULT_PAGE_SIZE, LOG_INFO, LOG_ERROR

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    user_name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    role_type = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    last_login_time = db.Column(db.DateTime)

    @staticmethod
    def data2dict(user):
        return {
            "UserID": user.user_id,
            "UserName": user.user_name,
            "RoleID": user.role_id,
            "RoleType": user.role_type,
            "CreateTime": user.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "LastLoginTime": user.last_login_time.strftime("%Y-%m-%d %H:%M:%S") if user.last_login_time else ""
        }

    @classmethod
    def check_admin(cls, install_param):
        admin = cls.query.filter_by(user_name="admin").first()
        if admin is None:
            if cls.query.count() != 0:
                RUN_LOG.log(LOG_ERROR, "DB may be corrupted, cannot find admin when start service.")
                click.secho("DB may be corrupted, cannot find admin.")
                return False
            if install_param.get("INIT_ADMIN_PASSWORD") is None:
                click.secho("Please set admin password in install param.")
                return False
            passwd, salt = pbkdf2hash(install_param.get("INIT_ADMIN_PASSWORD"), salt=None)
            admin = User(user_id=Admin_User, user_name="admin", password=passwd, salt=salt,
                         role_id=Admin_Role, role_type="admin", create_time=datetime.datetime.now())
            db.session.add(admin)
            db.session.commit()
            RUN_LOG.log(LOG_INFO, "Init Admin Success.")
        return True

    @classmethod
    def user_login(cls, user_name, password):
        user = cls.query.filter_by(user_name=user_name).first()
        if user is None:
            return status_code.USER_NOT_EXIST_ERROR, None
        if user.password == pbkdf2hash(password, user.salt)[0]:
            user.last_login_time = datetime.datetime.now()
            db.session.commit()
            return status_code.SUCCESS, cls.data2dict(user)
        return status_code.PASSWD_ERROR, None

    @classmethod
    def update_password(cls, password, new_password, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user is None:
            return status_code.USER_NOT_EXIST_ERROR
        if user.password == pbkdf2hash(password, user.salt)[0]:
            user.password, user.salt = pbkdf2hash(new_password)
            db.session.commit()
            return status_code.SUCCESS
        return status_code.PASSWD_ERROR

    @classmethod
    def reset_password(cls, user_name, new_password):
        if user_name == "admin":
            return status_code.PERMISSION_ERROR
        user = cls.query.filter_by(user_name=user_name).first()
        if user is None:
            return status_code.USER_NOT_EXIST_ERROR
        user.password, user.salt = pbkdf2hash(new_password)
        db.session.commit()
        return status_code.SUCCESS

    @classmethod
    def add_user(cls, user_name, password):
        if cls.query.count() >= MAX_USER_NUM:
            return status_code.MAX_USER_ERROR
        user = cls.query.filter_by(user_name=user_name).first()
        if user is not None:
            return status_code.USER_EXIST_ERROR
        passwd, salt = pbkdf2hash(password, salt=None)
        exist_ids = [user.user_id for user in cls.query.with_entities(cls.user_id).all()]
        for i in range(1, 501):
            if i not in exist_ids:
                new_user = User(user_id=i, user_name=user_name, password=passwd, salt=salt,
                                role_id=Normal_Role, role_type="normal", create_time=datetime.datetime.now())
                db.session.add(new_user)
                db.session.commit()
                return status_code.SUCCESS
        return status_code.MAX_USER_ERROR

    @classmethod
    def delete_user(cls, user_name):
        user = cls.query.filter_by(user_name=user_name).first()
        if user is None:
            return status_code.USER_NOT_EXIST_ERROR
        db.session.delete(user)
        db.session.commit()
        return status_code.SUCCESS

    @classmethod
    def get_user_by_name(cls, user_name):
        user = cls.query.filter_by(user_name=user_name).first()
        if user is None:
            return False, status_code.USER_NOT_EXIST_ERROR
        return True, user

    @classmethod
    def query_user(cls, current_page=DEFAULT_PAGE, pagesize=DEFAULT_PAGE_SIZE, user_name=None,
                   sort_by=None, sort_mode=None):
        sort_key_dict = {
            "UserID": cls.user_id,
            "UserName": cls.user_name,
            "CreateTime": cls.create_time,
            "LastLoginTime": cls.last_login_time
        }
        if user_name:
            users = cls.query.filter(cls.user_name.like("%" + user_name + "%"))
        else:
            users = cls.query
        if sort_by:
            if sort_mode == "desc":
                order = sort_key_dict.get(sort_by).desc()
            else:
                order = -sort_key_dict.get(sort_by).desc()
            users = users.order_by(order)
        total_count = users.count()
        try:
            paginate = users.paginate(page=current_page, per_page=pagesize)
        except NotFound:
            paginate = users.paginate(page=DEFAULT_PAGE, per_page=pagesize)
        user_list = [cls.data2dict(user) for user in paginate.items]
        page_count = len(user_list)
        return status_code.SUCCESS, {"users": user_list, "total": total_count, "page_total": page_count}

    def __repr__(self):
        return "<Users %r>" % self.user_name
