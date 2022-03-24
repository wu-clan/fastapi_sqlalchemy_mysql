#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends

from .api import api
from .casbin_rbac import casbin
from .depm import depm
from .role import role
from .test_redis import rd
from .user import user
from ..jwt_security import get_current_is_superuser
from ...common.sys_casbin import rbac

v1 = APIRouter(prefix='/v1')

v1.include_router(depm, prefix='/depm', tags=['部门管理'])
v1.include_router(api, prefix='/api', tags=['API管理'])
v1.include_router(role, prefix='/role', tags=['角色管理'])
v1.include_router(casbin, prefix='/rbac', tags=['RBAC-授权'], dependencies=[Depends(get_current_is_superuser)])
v1.include_router(user, prefix='/user', tags=['用户'])
v1.include_router(rd, prefix='/redis', tags=['测试-Redis'], dependencies=[Depends(rbac.verify_rbac)])
