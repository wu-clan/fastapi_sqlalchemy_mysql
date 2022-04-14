#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.datebase.base_class import Base


class Menu(Base):
    """ 菜单 """
    __tablename__ = 'sys_menu'
    name = Column(String(32), nullable=False, unique=True, comment='菜单展示名称')
    route_name = Column(String(32), nullable=False, comment='路由名称')
    route_path = Column(String(128), nullable=False, comment='路由路径')
    url = Column(String(128), nullable=False, comment='菜单url')
    parent_id = Column(Integer, comment='父级菜单id')
    sort = Column(Integer, nullable=False, comment='菜单排序')
    icon = Column(String(32), nullable=False, comment='菜单图标')
    file_path = Column(String(128), nullable=False, comment='前端文件路径')
    is_show = Column(Boolean(), nullable=False, comment='是否显示')
    roles = relationship('Role', secondary='sys_role_menu', backref='menus')


class RoleMenu(Base):
    """ 角色菜单 """
    __tablename__ = 'sys_role_menu'
    role_id = Column(Integer, ForeignKey('sys_role.id'), primary_key=True, comment='角色id')
    menu_id = Column(Integer, ForeignKey('sys_menu.id'), primary_key=True, comment='菜单id')
