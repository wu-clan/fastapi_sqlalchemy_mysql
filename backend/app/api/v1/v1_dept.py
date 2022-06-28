#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Query, Depends
from fastapi_pagination.ext.sqlalchemy import paginate

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_dept import DeptDao
from backend.app.schemas import Response200, Response403, Response404
from backend.app.schemas.sm_department import DeptCreate, DeptUpdate, DeptAll

dept = APIRouter()


@dept.get('', summary='获取所有部门', response_model=Page[DeptAll], dependencies=[Depends(get_current_user)])
def get_dept_list():
    return paginate(DeptDao.get_all_dept())


@dept.get('/{pk}', summary='获取指定部门', dependencies=[Depends(get_current_user)])
def get_one_dept(pk: int = Query(...)):
    check = DeptDao.get_one_dept_by_id(pk)
    if not check:
        return Response404()
    dept_user = DeptDao.get_dept_join_user_by_id(pk)
    if dept_user:
        return Response200(data=dept_user)
    return Response200(data=check)


@dept.post('', summary='创建部门', dependencies=[Depends(rbac.verify_rbac)])
def create_dept(obj: DeptCreate):
    check = DeptDao.get_one_dept_by_name(obj.name)
    if check:
        return Response403(msg='部门已存在, 请更换部门名称')
    else:
        data = DeptDao.create_dept(obj)
        return Response200(data=data)


@dept.put('/{pk}', summary='更新部门', dependencies=[Depends(rbac.verify_rbac)])
def create_dept(obj: DeptUpdate, pk: int = Query(...)):
    check = DeptDao.get_one_dept_by_id(pk)
    if not check:
        return Response404(data=obj)
    check_name = DeptDao.get_one_dept_by_name(obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='部门已存在, 请更换部门名称')
    DeptDao.update_dept(pk, obj)
    return Response200(data=obj)


@dept.delete('/{pk}', summary='删除部门', dependencies=[Depends(rbac.verify_rbac)])
def delete_dept(pk: int = Query(...)):
    check = DeptDao.get_one_dept_by_id(pk)
    if not check:
        return Response404()
    DeptDao.delete_dept(pk)
    return Response200()
