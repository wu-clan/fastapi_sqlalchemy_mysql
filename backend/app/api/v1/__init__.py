#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .captcha import captcha
from .test_crud import crud
from .test_jobs import aps
from .test_redis import rd
from .user import user

v1 = APIRouter(prefix='/v1')

v1.include_router(user, prefix='/user', tags=['用户'])
v1.include_router(captcha, prefix='/captcha', tags=['图片验证码'])
v1.include_router(rd, prefix='/redis', tags=['测试-Redis'])
v1.include_router(aps, prefix='/job', tags=['测试-APScheduler'])
v1.include_router(crud, prefix='/crud', tags=['仅用作补充测试CRUDBase'])
