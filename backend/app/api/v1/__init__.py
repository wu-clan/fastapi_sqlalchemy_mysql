#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends

from .v1_api import api
from .v1_casbin import casbin
from .v1_depm import depm
from .v1_role import role
from .v1_test_jobs import aps
from .v1_test_redis import rd
from .v1_user import user
from ..jwt_security import get_current_is_superuser
from ...common.sys_casbin import rbac

v1 = APIRouter(prefix='/v1')

v1.include_router(depm, prefix='/depm', tags=['部门管理'])
v1.include_router(api, prefix='/api', tags=['API管理'])
v1.include_router(role, prefix='/role', tags=['角色管理'])
v1.include_router(casbin, prefix='/rbac', tags=['RBAC-授权'], dependencies=[Depends(get_current_is_superuser)])
v1.include_router(user, prefix='/user', tags=['用户'])
v1.include_router(rd, prefix='/redis', tags=['测试-Redis'], dependencies=[Depends(rbac.verify_rbac)])
v1.include_router(aps, prefix='/job', tags=['测试-APScheduler'], dependencies=[Depends(get_current_is_superuser)])

