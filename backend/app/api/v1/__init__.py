#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends

from .v1_api import api
from .v1_casbin import casbin
from .v1_dept import dept
from .v1_role import role
from .v1_job import aps
from .v1_test_redis import rd
from .v1_user import user
from ..jwt_security import get_current_is_superuser
from ...common.sys_casbin import rbac

v1 = APIRouter(prefix='/v1')

v1.include_router(dept, tags=['部门管理'])
v1.include_router(api, tags=['API管理'])
v1.include_router(role, tags=['角色管理'])
v1.include_router(casbin, tags=['RBAC-授权'], dependencies=[Depends(get_current_is_superuser)])
v1.include_router(user, tags=['用户'])
v1.include_router(aps, tags=['任务'], dependencies=[Depends(get_current_is_superuser)])
v1.include_router(rd, prefix='/redis', tags=['测试-Redis'], dependencies=[Depends(rbac.verify_rbac)])
