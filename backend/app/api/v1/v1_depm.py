#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Query, Depends
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_depm import crud_depm
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response200, Response403, Response404, Response500
from backend.app.schemas.sm_department import DepmCreate, DepmUpdate, DepmAll

depm = APIRouter()


@depm.get('/all', summary='获取所有部门', response_model=Page[DepmAll], dependencies=[Depends(get_current_user)])
async def get_depm(db: AsyncSession = Depends(get_db)):
    return await paginate(db, crud_depm.get_all_depm())


@depm.post('/add', summary='创建部门', dependencies=[Depends(rbac.verify_rbac)])
async def create_depm(obj: DepmCreate):
    check = await crud_depm.get_one_depm_by_name(obj.name)
    if check:
        return Response403(msg='部门已存在')
    else:
        data = await crud_depm.create_depm(obj)
        return Response200(data=data)


@depm.put('/put/{id}', summary='修改部门', dependencies=[Depends(rbac.verify_rbac)])
async def update_depm(obj: DepmUpdate, id: int = Query(...)):
    check = await crud_depm.get_one_depm_by_id(id)
    if not check:
        return Response404(data=obj)
    check_name = await crud_depm.get_one_depm_by_name(obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='部门已存在, 请更换部门名称')
    data = await crud_depm.update_depm(id, obj)
    return Response200(data=data)


@depm.delete('/delete/{id}', summary='删除部门', dependencies=[Depends(rbac.verify_rbac)])
async def delete_depm(id: int = Query(...)):
    check = await crud_depm.get_one_depm_by_id(id)
    if not check:
        return Response404()
    if await crud_depm.delete_depm(id):
        return Response200()
    return Response500()
