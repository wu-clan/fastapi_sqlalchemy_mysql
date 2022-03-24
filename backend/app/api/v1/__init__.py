#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends

from .captcha import captcha
from .depm import depm
from .rbac_casbin import casbin
from .role import role
from .test_jobs import aps
from .test_redis import rd
from .user import user
from ..jwt_security import get_current_is_superuser
from ...common.sys_casbin import rbac

v1 = APIRouter(prefix='/v1')

v1.include_router(captcha, prefix='/captcha', tags=['图片验证码'])
v1.include_router(depm, prefix='/depm', tags=['部门管理'])
v1.include_router(role, prefix='/role', tags=['角色管理'])
v1.include_router(casbin, prefix='/rbac', tags=['RBAC-授权'], dependencies=[Depends(get_current_is_superuser)])
v1.include_router(user, prefix='/user', tags=['用户'])
v1.include_router(rd, prefix='/redis', tags=['测试-Redis'], dependencies=[Depends(rbac.verify_rbac)])
v1.include_router(aps, prefix='/job', tags=['测试-APScheduler'], dependencies=[Depends(rbac.verify_rbac)])
