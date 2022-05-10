#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, DateTime, func, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship

from backend.app.datebase.base_class import Base, use_uuid


class User(Base):
    """ 用户 """
    __tablename__ = 'sys_user'
    user_uid = Column(String(128), default=use_uuid, unique=True, comment='用户uid')
    username = Column(String(128), nullable=False, unique=True, index=True, comment='用户名')
    password = Column(String(128), nullable=False, comment='密码')
    email = Column(String(128), nullable=False, unique=True, index=True, comment='邮箱')
    is_superuser = Column(Boolean(), default=False, comment='超级权限')
    is_active = Column(Boolean(), default=True, comment='用户账号状态')
    avatar = Column(String(256), default=None, comment='头像')
    mobile_number = Column(String(16), default=None, comment='手机号')
    wechat = Column(String(128), default=None, comment='微信')
    qq = Column(String(128), default=None, comment='QQ')
    blog_address = Column(String(128), default=None, comment='博客地址')
    introduction = Column(LONGTEXT, default=None, comment='自我介绍')
    time_joined = Column(DateTime, server_default=func.now(), comment='注册时间')
    last_login = Column(DateTime, server_default=None, onupdate=func.now(), comment='上次登录时间')
    department_id = Column(Integer, ForeignKey('sys_department.id'), comment='部门关联id')
    department = relationship('Department', backref='users')
