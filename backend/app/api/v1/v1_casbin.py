#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_casbin import crud_rbac
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response200, Response404, Response403
from backend.app.schemas.sm_casbin import PolicyCreate, PolicyUpdate, PolicyDelete, RBACAll, UserRole

casbin = APIRouter()


@casbin.get('/all', summary='获取所有权限规则', response_model=Page[RBACAll])
async def get_all_rbac(db: AsyncSession = Depends(get_db)):
    return await paginate(db, crud_rbac.get_all_rbac())


@casbin.get('/get_policy', summary='获取p策略')
def get_policy():
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.get_policy()
    if data:
        return Response200(data=data)


@casbin.post('/add_policy', summary='添加基于角色(主)/用户(次)的访问权限')
def create_policy(p: PolicyCreate):
    """
    p策略:

    - 推荐添加基于角色的访问权限, 需配合添加g策略才能真正拥有访问权限<br>
    **格式**: 角色role + 访问路径path + 访问方法method

    - 如果添加基于用户的访问权限, 不需配合添加g策略就能真正拥有权限<br>
    **格式**: 用户uid + 访问路径path + 访问方法method
    """
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.add_policy(p.sub, p.path, p.method)
    if data:
        return Response200(data=data)
    else:
        return Response403(msg='添加失败,访问权限已存在', data=data)


@casbin.put('/update_policy', summary='更新基于角色(主)/用户(次)的访问权限')
def update_policy(p_old: PolicyUpdate, p_new: PolicyUpdate):
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


@casbin.get('/get_group', summary='获取g策略')
def get_group():
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.get_grouping_policy()
    if data:
        return Response200(data=data)


@casbin.post('/add_group', summary='添加基于用户组的访问权限')
def create_group(p: UserRole):
    """
    g策略 (**依赖p策略**):

    - 如果在p策略中添加了基于角色的访问权限, 则还需要在g策略中添加基于用户组的访问权限, 才能真正拥有访问权限<br>
    **格式**: 用户uid + 角色role

    - 如果在p策略中添加了基于用户的访问权限, 则不添加相应的g策略也能真正拥有访问权限<br>
    但是拥有的不是用户角色的所有权限, 而只是单一的对应的p策略所添加的访问权限
    """
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
