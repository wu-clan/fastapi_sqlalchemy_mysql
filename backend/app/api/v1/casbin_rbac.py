#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import APIRouter

from backend.app.common.sys_casbin import rbac
from backend.app.schemas import Response200, Response404, Response403
from backend.app.schemas.sm_casbin import RBACCreate, RBACDelete

casbin = APIRouter()


@casbin.get('/rbac/all', summary='获取所有权限规则')
def get_rbac():
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.get_policy()
    if data:
        return Response200(data=data)
    else:
        return Response404(msg='授权规则为空')


@casbin.post('/rbac/add_policy', summary='添加访问权限')
def create_policy(p: RBACCreate):
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.add_policy(p.role, p.path, p.method)
    if data:
        return Response200(data=data)
    else:
        return Response403(msg='添加失败,访问权限已存在', data=data)


@casbin.delete('/rbac/del_policy', summary='删除访问权限')
def delete_policy(p: RBACDelete):
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.remove_policy(p.role, p.path, p.method)
    if data:
        return Response200(data=data)
    else:
        return Response404(msg='删除失败,访问权限不存在', data=data)
