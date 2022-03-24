#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String

from backend.app.datebase.base_class import Base


class Role(Base):
    """ 角色 """
    __tablename__ = 'role'
    name = Column(String(32), nullable=False, unique=True, comment='角色名称')
    description = Column(String(256), comment='角色描述')
