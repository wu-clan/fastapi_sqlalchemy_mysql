#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from backend.app.datebase.base_class import Base


class Menu(Base):
    """ 菜单 (未使用) """
    __tablename__ = 'sys_menu'
    parent_id = Column(Integer, comment='父级菜单id')
    name = Column(String(32), nullable=False, comment='菜单名称')
    url = Column(String(128), nullable=False, comment='菜单url')
    icon = Column(String(128), nullable=False, comment='菜单图标')
    sort = Column(Integer, nullable=False, comment='菜单排序')
