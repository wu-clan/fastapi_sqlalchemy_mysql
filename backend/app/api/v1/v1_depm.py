#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Query, Depends
from fastapi_pagination.ext.sqlalchemy import paginate

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_depm import crud_depm
from backend.app.schemas import Response200, Response403, Response404
from backend.app.schemas.sm_department import DepmCreate, DepmUpdate, DepmAll

depm = APIRouter()


@depm.get('/all', summary='获取所有部门', response_model=Page[DepmAll], dependencies=[Depends(get_current_user)])
def get_depm():
    return paginate(crud_depm.get_all_depm())


@depm.get('/{id}', summary='获取指定部门', dependencies=[Depends(get_current_user)])
def get_one_depm(id: int = Query(...)):
    check = crud_depm.get_one_depm_by_id(id)
    if not check:
        return Response404()
    depm_user = crud_depm.get_depm_join_user_by_id(id)
    return Response200(data=depm_user)


@depm.post('/add', summary='创建部门', dependencies=[Depends(rbac.verify_rbac)])
def create_depm(obj: DepmCreate):
    check = crud_depm.get_one_depm_by_name(obj.name)
    if check:
        return Response403(msg='部门已存在, 请更换部门名称')
    else:
        data = crud_depm.create_depm(obj)
        return Response200(data=data)


@depm.put('/put/{id}', summary='修改部门', dependencies=[Depends(rbac.verify_rbac)])
def create_depm(obj: DepmUpdate, id: int = Query(...)):
    check = crud_depm.get_one_depm_by_id(id)
    if not check:
        return Response404(data=obj)
    check_name = crud_depm.get_one_depm_by_name(obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='部门已存在, 请更换部门名称')
    crud_depm.update_depm(id, obj)
    return Response200(data=obj)


@depm.delete('/delete/{id}', summary='删除部门', dependencies=[Depends(rbac.verify_rbac)])
def get_depm(id: int = Query(...)):
    check = crud_depm.get_one_depm_by_id(id)
    if not check:
        return Response404()
    crud_depm.delete_depm(id)
    return Response200()
