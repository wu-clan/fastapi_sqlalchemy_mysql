#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .captcha import captcha
from .rbac_casbin import casbin
from .test_crud import crud
from .test_jobs import aps
from .test_redis import rd
from .user import user

v1 = APIRouter(prefix='/v1')

v1.include_router(user, tags=['用户'])
v1.include_router(captcha, tags=['图片验证码'])
v1.include_router(casbin, tags=['RBAC-授权'])
v1.include_router(rd, tags=['测试-Redis'])
v1.include_router(aps, tags=['测试-APScheduler'])
v1.include_router(crud, tags=['仅用作补充测试CRUDBase'])
