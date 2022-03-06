#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .rbac_casbin import casbin
from .test_redis import rd
from .user import user

v1 = APIRouter(prefix='/v1')

v1.include_router(user, tags=['用户'])
v1.include_router(rd, tags=['测试-Redis'])
v1.include_router(casbin, tags=['RBAC-授权'])
