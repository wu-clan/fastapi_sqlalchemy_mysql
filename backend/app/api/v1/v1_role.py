#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.api_crud import api_crud
from backend.app.crud.role_crud import role_crud
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response404, Response403, Response200, Response500
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate, RoleAll

role = APIRouter()


@role.get('/all', summary='获取所有角色', response_model=Page[RoleAll], dependencies=[Depends(get_current_user)])
async def get_all_role(db: AsyncSession = Depends(get_db)):
    return await paginate(db, role_crud.get_all_role())


@role.post('/add', summary='创建角色', dependencies=[Depends(rbac.verify_rbac)])
async def create_depm(obj: RoleCreate, db: AsyncSession = Depends(get_db)):
    check = await role_crud.get_one_role_by_name(db, obj.name)
    if check:
        return Response403(msg='角色已存在')
    else:
        data = await role_crud.create_role(db, obj)
        return Response200(data=data)


@role.put('/put/{id}', summary='修改角色', dependencies=[Depends(rbac.verify_rbac)])
async def create_depm(obj: RoleUpdate, id: int = Query(...), db: AsyncSession = Depends(get_db)):
    check = await role_crud.get_one_role_by_id(db, id)
    if not check:
        return Response404(data=obj)
    check_name = await role_crud.get_one_role_by_name(db, obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='角色已存在, 请更换角色名称')
    data = await role_crud.update_role(db, id, obj)
    return Response200(data=data)


@role.delete('/delete/{id}', summary='删除角色', dependencies=[Depends(rbac.verify_rbac)])
async def get_depm(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    check = await role_crud.get_one_role_by_id(db, id)
    if not check:
        return Response404()
    if await role_crud.delete_role(db, id):
        return Response200()
    return Response500()
