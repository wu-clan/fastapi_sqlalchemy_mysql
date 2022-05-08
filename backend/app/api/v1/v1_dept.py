#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Query, Depends
from fastapi_pagination.ext.sqlalchemy import paginate

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_dept import crud_dept
from backend.app.schemas import Response200, Response403, Response404
from backend.app.schemas.sm_department import DeptCreate, DeptUpdate, DeptAll

dept = APIRouter()


@dept.get('/all', summary='获取所有部门', response_model=Page[DeptAll], dependencies=[Depends(get_current_user)])
def get_dept():
    return paginate(crud_dept.get_all_dept())


@dept.get('/{id}', summary='获取指定部门', dependencies=[Depends(get_current_user)])
def get_one_dept(id: int = Query(...)):
    check = crud_dept.get_one_dept_by_id(id)
    if not check:
        return Response404()
    dept_user = crud_dept.get_dept_join_user_by_id(id)
    return Response200(data=dept_user)


@dept.post('/add', summary='创建部门', dependencies=[Depends(rbac.verify_rbac)])
def create_dept(obj: DeptCreate):
    check = crud_dept.get_one_dept_by_name(obj.name)
    if check:
        return Response403(msg='部门已存在, 请更换部门名称')
    else:
        data = crud_dept.create_dept(obj)
        return Response200(data=data)


@dept.put('/put/{id}', summary='更新部门', dependencies=[Depends(rbac.verify_rbac)])
def create_dept(obj: DeptUpdate, id: int = Query(...)):
    check = crud_dept.get_one_dept_by_id(id)
    if not check:
        return Response404(data=obj)
    check_name = crud_dept.get_one_dept_by_name(obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='部门已存在, 请更换部门名称')
    crud_dept.update_dept(id, obj)
    return Response200(data=obj)


@dept.delete('/delete/{id}', summary='删除部门', dependencies=[Depends(rbac.verify_rbac)])
def get_dept(id: int = Query(...)):
    check = crud_dept.get_one_dept_by_id(id)
    if not check:
        return Response404()
    crud_dept.delete_dept(id)
    return Response200()
