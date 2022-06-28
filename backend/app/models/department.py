#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String

from backend.app.database.base_class import Base


class Department(Base):
    """ 部门 """
    __tablename__ = 'sys_department'
    name = Column(String(32), nullable=False, unique=True, comment='部门名称')
    description = Column(String(256), comment='部门描述')
