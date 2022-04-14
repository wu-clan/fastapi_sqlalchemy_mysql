#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String

from backend.app.datebase.base_class import Base


class API(Base):
    """ 系统api """
    __tablename__ = 'sys_api'
    path = Column(String(128), nullable=False, unique=True, comment='api路径')
    group = Column(String(32), comment='api分组')
    description = Column(String(128), comment='api描述')
    method = Column(String(16), nullable=False, comment='请求方法')
