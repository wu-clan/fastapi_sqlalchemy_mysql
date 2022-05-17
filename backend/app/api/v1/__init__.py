#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .v1_captcha import captcha
from .v1_test_crud import crud
from .v1_job import aps
from .v1_test_redis import rd
from .v1_user import user

v1 = APIRouter(prefix='/v1')

v1.include_router(captcha, prefix='/captchas', tags=['图片验证码'])
v1.include_router(user, prefix='/users', tags=['用户'])
v1.include_router(aps, prefix='/tasks', tags=['任务'])
v1.include_router(rd, prefix='/redis', tags=['测试-Redis'])
v1.include_router(crud, prefix='/crud/test/users', tags=['仅用作补充测试CRUDBase'])
