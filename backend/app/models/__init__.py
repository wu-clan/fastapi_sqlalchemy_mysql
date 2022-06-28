#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入所有模型，并将 Base 放在最前面， 以便 Base 拥有它们

Imported by Alembic
"""
from backend.app.database.base_class import Base
from backend.app.models.api import API
from backend.app.models.casbin_rule import CasbinRule
from backend.app.models.department import Department
from backend.app.models.user import User
from backend.app.models.role import Role
from backend.app.models.menu import Menu
