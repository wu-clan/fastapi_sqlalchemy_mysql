#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Query, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.depm_crud import depm_crud
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response200, Response403, Response404, Response500
from backend.app.schemas.sm_department import DepmCreate, DepmUpdate, DepmAll

depm = APIRouter()


@depm.get('/all', summary='获取所有部门', response_model=Page[DepmAll], dependencies=[Depends(get_current_user)])
async def get_depm(db: Session = Depends(get_db)):
    return paginate(depm_crud.get_all_depm(db))


@depm.post('/add', summary='创建部门', dependencies=[Depends(rbac.verify_rbac)])
async def create_depm(obj: DepmCreate, db: Session = Depends(get_db)):
    check = depm_crud.get_one_depm_by_name(db, obj.name)
    print(check)
    if check:
        return Response403(msg='部门已存在')
    else:
        data = depm_crud.create_depm(db, obj)
        return Response200(data=data)


@depm.put('/put/{id}', summary='修改部门', dependencies=[Depends(rbac.verify_rbac)])
async def create_depm(obj: DepmUpdate, id: int = Query(...), db: Session = Depends(get_db)):
    check = depm_crud.get_one_depm_by_id(db, id)
    if not check:
        return Response404(data=obj)
    check_name = depm_crud.get_one_depm_by_name(db, obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='部门已存在, 请更换部门名称')
    data = depm_crud.update_depm(db, id, obj)
    return Response200(data=data)


@depm.delete('/delete/{id}', summary='删除部门', dependencies=[Depends(rbac.verify_rbac)])
async def get_depm(id: int = Query(...), db: Session = Depends(get_db)):
    check = depm_crud.get_one_depm_by_id(db, id)
    if not check:
        return Response404()
    if depm_crud.delete_depm(db, id):
        return Response200()
    return Response500()
