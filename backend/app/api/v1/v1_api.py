#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from fastapi_pagination.ext.sqlalchemy import paginate

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_api import crud_api
from backend.app.schemas import Response404, Response403, Response200, Response500
from backend.app.schemas.sm_api import APIAll, APICreate, APIUpdate

api = APIRouter()


@api.get('', summary='获取所有API', response_model=Page[APIAll], dependencies=[Depends(get_current_user)])
def get_api_list():
    return paginate(crud_api.get_all_api())


@api.post('', summary='创建API', dependencies=[Depends(rbac.verify_rbac)])
def create_api(obj: APICreate):
    check = crud_api.get_one_api_by_path(obj.path)
    if check:
        return Response403(msg='API已存在')
    else:
        data = crud_api.create_api(obj)
        return Response200(data=data)


@api.put('/{id}', summary='更新API', dependencies=[Depends(rbac.verify_rbac)])
def update_api(obj: APIUpdate, id: int = Query(...)):
    check = crud_api.get_one_api_by_id(id)
    if not check:
        return Response404(data=obj)
    check_path = crud_api.get_one_api_by_path(obj.path)
    if obj.path != check.path:
        if check_path:
            return Response403(msg='API已存在, 请更换API名称')
    crud_api.update_api(id, obj)
    return Response200(data=obj)


@api.delete('/{id}', summary='删除API', dependencies=[Depends(rbac.verify_rbac)])
def delete_api(id: int = Query(...)):
    check = crud_api.get_one_api_by_id(id)
    if not check:
        return Response404()
    if crud_api.delete_api(id):
        return Response200()
    return Response500()
