#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .test_redis import rd
from .user import user

v1 = APIRouter(prefix='/v1')

v1.include_router(user, prefix='/user', tags=['用户'])
v1.include_router(rd, prefix='/redis', tags=['测试-Redis'])