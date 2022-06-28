#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_menu import MenuDao
from backend.app.crud.crud_role import RoleDao
from backend.app.database.db_mysql import get_db
from backend.app.schemas import Response404, Response403, Response200
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate, RoleAll, RoleMenuCreate

role = APIRouter()


@role.get('', summary='获取所有角色', response_model=Page[RoleAll], dependencies=[Depends(get_current_user)])
def get_role_list():
    with get_db() as session:
        return paginate(session, RoleDao.get_all_role())


@role.post('', summary='创建角色', dependencies=[Depends(rbac.verify_rbac)])
def create_role(obj_role: RoleCreate, obj_menu: RoleMenuCreate):
    check = RoleDao.get_one_role_by_name(obj_role.name)
    if check:
        return Response403(msg='角色已存在')
    if len(obj_menu.menu_id) < 1:
        raise HTTPException(status_code=403, detail='必须至少选择一个菜单')
    if len(obj_menu.menu_id) == 1:
        if not MenuDao.get_one_menu_by_id(obj_menu.menu_id[0]):
            raise HTTPException(status_code=404, detail=f'所选菜单 {obj_menu.menu_id[0]} 不存在')
    elif len(obj_menu.menu_id) > 1:
        for _ in obj_menu.menu_id:
            if not MenuDao.get_one_menu_by_id(_):
                raise HTTPException(status_code=404, detail=f'所选菜单 {_} 不存在')
    data = RoleDao.create_role(obj_role, obj_menu)
    return Response200(data={'role': data, 'menu': obj_menu.menu_id})


@role.put('/{pk}', summary='更新角色', dependencies=[Depends(rbac.verify_rbac)])
def create_role(obj_role: RoleUpdate, obj_menu: RoleMenuCreate, pk: int = Query(...)):
    check = RoleDao.get_one_role_by_id(pk)
    if not check:
        return Response404(data=obj_role)
    check_name = RoleDao.get_one_role_by_name(obj_role.name)
    if obj_role.name != check.name:
        if check_name:
            return Response403(msg='角色已存在, 请更换角色名称')
    if len(obj_menu.menu_id) < 1:
        raise HTTPException(status_code=403, detail='必须至少选择一个菜单')
    if len(obj_menu.menu_id) == 1:
        if not MenuDao.get_one_menu_by_id(obj_menu.menu_id[0]):
            raise HTTPException(status_code=404, detail=f'所选菜单 {obj_menu.menu_id[0]} 不存在')
    elif len(obj_menu.menu_id) > 1:
        for _ in obj_menu.menu_id:
            if not MenuDao.get_one_menu_by_id(_):
                raise HTTPException(status_code=404, detail=f'所选菜单 {_} 不存在')
    data = RoleDao.update_role(pk, obj_role, obj_menu)
    return Response200(data={'role': data, 'menu': obj_menu.menu_id})


@role.delete('/{pk}', summary='删除角色', dependencies=[Depends(rbac.verify_rbac)])
def get_role(pk: int = Query(...)):
    check = RoleDao.get_one_role_by_id(pk)
    if not check:
        return Response404()
    RoleDao.delete_role(pk)
    return Response200()
