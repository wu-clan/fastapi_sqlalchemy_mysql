#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.common.pagination import Page
from backend.app.crud.api_crud import api_crud
from backend.app.crud.role_crud import role_crud
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response404, Response403, Response200, Response500
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate, RoleAll

role = APIRouter()


@role.get('/role/all', summary='获取所有角色', response_model=Page[RoleAll])
async def get_all_role(db: AsyncSession = Depends(get_db)):
    return await paginate(db, role_crud.get_all_role())


@role.post('/role/add', summary='创建角色')
async def create_depm(obj: RoleCreate, db: AsyncSession = Depends(get_db)):
    check = await role_crud.get_one_role_by_name(db, obj.name)
    if check:
        return Response403(msg='角色已存在')
    for _ in obj.api_id.split(','):
        if not await api_crud.get_one_api_by_id(db, _):
            return Response404(data=_)
    else:
        data = await role_crud.create_depm(db, obj)
        return Response200(data=data)


@role.put('/role/put/{id}', summary='修改角色')
async def create_depm(obj: RoleUpdate, id: int = Query(...), db: AsyncSession = Depends(get_db)):
    check = await role_crud.get_one_role_by_id(db, id)
    if not check:
        return Response404(data=obj)
    check_name = await role_crud.get_one_role_by_name(db, obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='角色已存在, 请更换角色名称')
    for _ in obj.api_id.split(','):
        if not await api_crud.get_one_api_by_id(db, _):
            return Response404(data=_)
    data = await role_crud.update_role(db, id, obj)
    return Response200(data=data)


@role.delete('/role/delete/{id}', summary='删除角色')
async def get_depm(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    check = await role_crud.get_one_role_by_id(db, id)
    if not check:
        return Response404()
    if await role_crud.delete_role(db, id):
        return Response200()
    return Response500()
