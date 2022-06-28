#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends

from .v1_api import api
from .v1_captcha import captcha
from .v1_dept import dept
from .v1_casbin import casbin
from .v1_menu import menu
from .v1_role import role
from .v1_job import aps
from .v1_test_redis import rd
from .v1_user import user
from ..jwt_security import get_current_is_superuser
from ...common.sys_casbin import rbac

v1 = APIRouter(prefix='/v1')

v1.include_router(captcha, prefix='/captcha', tags=['图片验证码'])
v1.include_router(dept, prefix='/depts', tags=['部门管理'])
v1.include_router(api, prefix='/apis', tags=['API管理'])
v1.include_router(role, prefix='/roles', tags=['角色管理'])
v1.include_router(menu, prefix='/menus', tags=['菜单管理'])
v1.include_router(casbin, prefix='/rbac', tags=['RBAC-授权'], dependencies=[Depends(get_current_is_superuser)])
v1.include_router(user, prefix='/users', tags=['用户'])
v1.include_router(aps, prefix='/tasks', tags=['任务'], dependencies=[Depends(rbac.verify_rbac)])
v1.include_router(rd, prefix='/redis', tags=['测试-Redis'], dependencies=[Depends(rbac.verify_rbac)])
