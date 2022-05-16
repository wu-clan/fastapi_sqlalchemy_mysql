#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .v1_captcha import captcha
from .v1_test_redis import rd
from .v1_user import user

v1 = APIRouter(prefix='/v1')

v1.include_router(captcha, tags=['图片验证码'])
v1.include_router(user, tags=['用户'])
v1.include_router(rd, prefix='/redis', tags=['测试-Redis'])
