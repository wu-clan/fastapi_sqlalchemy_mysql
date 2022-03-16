#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.common.pagination import Page
from backend.app.crud.api_crud import api_crud

from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response404, Response403, Response200, Response500
from backend.app.schemas.sm_api import APIAll, APICreate, APIUpdate

api = APIRouter()


@api.get('/api/all', summary='获取所有API', response_model=Page[APIAll])
async def get_api(db: AsyncSession = Depends(get_db)):
    return await paginate(db, api_crud.get_all_api())


@api.post('/api/add', summary='创建API')
async def create_depm(obj: APICreate, db: AsyncSession = Depends(get_db)):
    check = await api_crud.get_one_api_by_name(db, obj.path)
    if check:
        return Response403(msg='API已存在')
    else:
        data = await api_crud.create_api(db, obj)
        return Response200(data=data)


@api.put('/role/api/{id}', summary='修改API')
async def create_depm(obj: APIUpdate, id: int = Query(...), db: AsyncSession = Depends(get_db)):
    check = await api_crud.get_one_api_by_id(db, id)
    if not check:
        return Response404(data=obj)
    check_path = await api_crud.get_one_api_by_name(db, obj.path)
    if obj.path != check.path:
        if check_path:
            return Response403(msg='API已存在, 请更换API名称')
    data = await api_crud.update_api(db, id, obj)
    return Response200(data=data)


@api.delete('/api/delete/{id}', summary='删除API')
async def get_depm(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    check = await api_crud.get_one_api_by_id(db, id)
    if not check:
        return Response404()
    if await api_crud.delete_api(db, id):
        return Response200()
    return Response500()
