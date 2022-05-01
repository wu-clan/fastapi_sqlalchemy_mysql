#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_menu import crud_menu
from backend.app.crud.crud_role import crud_role
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response404, Response403, Response200
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate, RoleAll, RoleMenuCreate

role = APIRouter()


@role.get('/all', summary='获取所有角色', response_model=Page[RoleAll], dependencies=[Depends(get_current_user)])
def get_all_role(db: Session = Depends(get_db)):
    return paginate(db, crud_role.get_all_role())


@role.post('/add', summary='创建角色', dependencies=[Depends(rbac.verify_rbac)])
def create_depm(obj: RoleCreate, menu: RoleMenuCreate):
    check = crud_role.get_one_role_by_name(obj.name)
    if check:
        return Response403(msg='角色已存在')
    if len(menu.menu_id) < 1:
        raise HTTPException(status_code=403, detail='必须至少选择一个菜单')
    if len(menu.menu_id) == 1:
        if not crud_menu.get_one_menu_by_id(menu.menu_id[0]):
            raise HTTPException(status_code=404, detail=f'所选菜单 {menu.menu_id[0]} 不存在')
    elif len(menu.menu_id) > 1:
        for _ in menu.menu_id:
            if not crud_menu.get_one_menu_by_id(_):
                raise HTTPException(status_code=404, detail=f'所选菜单 {_} 不存在')
    data = crud_role.create_role(obj, menu)
    return Response200(data={'role': data, 'menu': menu.menu_id})


@role.put('/put/{id}', summary='修改角色', dependencies=[Depends(rbac.verify_rbac)])
def create_depm(obj: RoleUpdate, menu: RoleMenuCreate, id: int = Query(...)):
    check = crud_role.get_one_role_by_id(id)
    if not check:
        return Response404(data=obj)
    check_name = crud_role.get_one_role_by_name(obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='角色已存在, 请更换角色名称')
    if len(menu.menu_id) < 1:
        raise HTTPException(status_code=403, detail='必须至少选择一个菜单')
    if len(menu.menu_id) == 1:
        if not crud_menu.get_one_menu_by_id(menu.menu_id[0]):
            raise HTTPException(status_code=404, detail=f'所选菜单 {menu.menu_id[0]} 不存在')
    elif len(menu.menu_id) > 1:
        for _ in menu.menu_id:
            if not crud_menu.get_one_menu_by_id(_):
                raise HTTPException(status_code=404, detail=f'所选菜单 {_} 不存在')
    data = crud_role.update_role(id, obj, menu)
    return Response200(data={'role': data, 'menu': menu.menu_id})


@role.delete('/delete/{id}', summary='删除角色', dependencies=[Depends(rbac.verify_rbac)])
def get_depm(id: int = Query(...)):
    check = crud_role.get_one_role_by_id(id)
    if not check:
        return Response404()
    crud_role.delete_role(id)
    return Response200()
