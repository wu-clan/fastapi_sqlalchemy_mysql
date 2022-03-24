#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 导入所有模型，并将 Base 放在最前面， 以便 Base 拥有它们
# imported by Alembic
"""
from backend.app.datebase.base_class import Base
from backend.app.model.casbin_rule import CasbinRule
from backend.app.model.department import Department
from backend.app.model.user import User
from backend.app.model.role import Role
