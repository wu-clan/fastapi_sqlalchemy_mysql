#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Query, Depends
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_dept import crud_dept
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response200, Response403, Response404, Response500
from backend.app.schemas.sm_department import DeptCreate, DeptUpdate, DeptAll

dept = APIRouter()


@dept.get('/all', summary='获取所有部门', response_model=Page[DeptAll], dependencies=[Depends(get_current_user)])
async def get_all_dept(db: AsyncSession = Depends(get_db)):
    return await paginate(db, crud_dept.get_all_dept())


@dept.post('/add', summary='创建部门', dependencies=[Depends(rbac.verify_rbac)])
async def create_dept(obj: DeptCreate):
    check = await crud_dept.get_one_dept_by_name(obj.name)
    if check:
        return Response403(msg='部门已存在')
    else:
        data = await crud_dept.create_dept(obj)
        return Response200(data=data)


@dept.put('/put/{id}', summary='修改部门', dependencies=[Depends(rbac.verify_rbac)])
async def update_dept(obj: DeptUpdate, id: int = Query(...)):
    check = await crud_dept.get_one_dept_by_id(id)
    if not check:
        return Response404(data=obj)
    check_name = await crud_dept.get_one_dept_by_name(obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='部门已存在, 请更换部门名称')
    data = await crud_dept.update_dept(id, obj)
    return Response200(data=data)


@dept.delete('/delete/{id}', summary='删除部门', dependencies=[Depends(rbac.verify_rbac)])
async def delete_dept(id: int = Query(...)):
    check = await crud_dept.get_one_dept_by_id(id)
    if not check:
        return Response404()
    if await crud_dept.delete_dept(id):
        return Response200()
    return Response500()
