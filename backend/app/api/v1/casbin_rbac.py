#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.casbin_crud import rbac_crud
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response200, Response404, Response403
from backend.app.schemas.sm_casbin import RBACCreate, RBACDelete, RBACAll

casbin = APIRouter()


@casbin.get('/all', summary='获取所有权限规则', response_model=Page[RBACAll])
async def get_rbac(db: AsyncSession = Depends(get_db)):
    return await paginate(db, rbac_crud.get_all_rbac())


@casbin.post('/add_policy', summary='添加访问权限')
def create_policy(p: RBACCreate):
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.add_policy(p.role, p.path, p.method)
    if data:
        return Response200(data=data)
    else:
        return Response403(msg='添加失败,访问权限已存在', data=data)


@casbin.delete('/del_policy', summary='删除访问权限')
def delete_policy(p: RBACDelete):
    enforcer = rbac.get_casbin_enforcer()
    data = enforcer.remove_policy(p.role, p.path, p.method)
    if data:
        return Response200(data=data)
    else:
        return Response404(msg='删除失败,访问权限不存在', data=data)
