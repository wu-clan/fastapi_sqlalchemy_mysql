#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String

from backend.app.datebase.base_class import Base


class API(Base):
    """ 系统api """
    __tablename__ = 'api'
    path = Column(String(256), nullable=False, unique=True, comment='api路径')
    description = Column(String(128), comment='api描述')
    method = Column(String(16), comment='请求方法')
