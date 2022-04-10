#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.casbin_crud import rbac_crud
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response200, Response404, Response403
from backend.app.schemas.sm_casbin import PolicyCreate, PolicyUpdate, PolicyDelete, RBACAll, UserRole

casbin = APIRouter()


@casbin.get('/all', summary='获取所有权限规则', response_model=Page[RBACAll])
async def get_rbac(db: Session = Depends(get_db)):
    return paginate(rbac_crud.get_all_rbac(db))


@casbin.post('/add_policy', summary='添加基于角色(主)/用户(次)的访问权限',
             description='此项为p策略,如果添加基于用户的权限,必须使用用户uid,但是推荐基于角色授权')
def create_policy(p: PolicyCreate):
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.add_policy(p.sub, p.path, p.method)
    if data:
        return Response200(data=data)
    else:
        return Response403(msg='添加失败,访问权限已存在', data=data)


@casbin.put('/update_policy', summary='更新基于角色(主)/用户(次)的访问权限')
def update_group(p_old: PolicyUpdate, p_new: PolicyUpdate):
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.update_policy([p_old.sub, p_old.path, p_old.method], [p_new.sub, p_new.path, p_new.method])
    if data:
        return Response200(data=data)
    else:
        return Response404(msg=f'更新失败,访问权限v0 {p_old.sub} 不存在', data=data)


@casbin.delete('/del_policy', summary='删除基于角色(主)/用户(次)的访问权限')
def delete_policy(p: PolicyDelete):
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.remove_policy(p.sub, p.path, p.method)
    if data:
        return Response200(data=data)
    else:
        return Response404(msg='删除失败,访问权限不存在', data=data)


@casbin.post('/add_group', summary='添加基于用户组的访问权限',
             description='依赖p策略,如果未添加基于用户的p策略,但是添加了基于角色的p策略,则必须添加此策略才能完成用户授权,推荐使用,格式必须为: 用户uid + 角色role')
def create_group(p: UserRole):
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.add_grouping_policy(p.uid, p.role)
    if data:
        return Response200(data=data)
    else:
        return Response403(msg='添加失败,访问权限已存在', data=data)


@casbin.delete('/del_group', summary='删除基于用户组的访问权限')
def delete_group(p: UserRole):
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.remove_grouping_policy(p.uid, p.role)
    if data:
        return Response200(data=data)
    else:
        return Response404(msg='删除失败,访问权限不存在', data=data)
