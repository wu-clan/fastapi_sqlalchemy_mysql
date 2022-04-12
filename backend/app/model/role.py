#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.datebase.base_class import Base


class Role(Base):
    """ 角色 """
    __tablename__ = 'sys_role'
    name = Column(String(32), nullable=False, unique=True, comment='角色名称')
    api_id = Column(String(256), comment='api_id')
    users = relationship('User', secondary='sys_user_role', backref='roles')


class User_Role(Base):
    """ 用户角色 """
    __tablename__ = 'sys_user_role'
    user_id = Column(Integer, ForeignKey('sys_user.id'), primary_key=True, comment='用户id')
    role_id = Column(Integer, ForeignKey('sys_role.id'), primary_key=True, comment='角色id')
