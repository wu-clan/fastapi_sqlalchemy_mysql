#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter

from backend.app.common.sys_casbin import get_casbin_enforcer
from backend.app.schemas import Response200, Response404, Response403
from backend.app.schemas.sm_rbac import RBACCreate, RBACDelete

casbin = APIRouter()


@casbin.get('/rbac_list', summary='获取所有权限规则')
def get_rbac():
    e = get_casbin_enforcer()
    _rbac = e.get_policy()
    if _rbac:
        return Response200(data=_rbac)
    else:
        return Response404(msg='授权规则为空')


@casbin.post('/add_policy', summary='添加访问权限')
def create_policy(p: RBACCreate):
    e = get_casbin_enforcer()
    _pl = e.add_policy(p.sub, p.path, p.method)
    if _pl:
        return Response200(data=_pl)
    else:
        return Response403(msg='添加失败,访问权限已存在', data=_pl)


@casbin.delete('/del_policy', summary='删除访问权限')
def delete_policy(p: RBACDelete):
    e = get_casbin_enforcer()
    _pl = e.remove_policy(p.sub, p.path, p.method)
    if _pl:
        return Response200(data=_pl)
    else:
        return Response404(msg='删除失败,访问权限不存在', data=_pl)
