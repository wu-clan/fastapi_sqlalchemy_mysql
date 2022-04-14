#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.menu_crud import menu_crud
from backend.app.crud.role_crud import role_crud
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response404, Response403, Response200
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate, RoleAll, RoleMenuCreate

role = APIRouter()


@role.get('/all', summary='获取所有角色', response_model=Page[RoleAll], dependencies=[Depends(get_current_user)])
def get_all_role(db: Session = Depends(get_db)):
    return paginate(db, role_crud.get_all_role())


@role.post('/add', summary='创建角色', dependencies=[Depends(rbac.verify_rbac)])
def create_depm(obj: RoleCreate, menu: RoleMenuCreate, db: Session = Depends(get_db)):
    check = role_crud.get_one_role_by_name(db, obj.name)
    if check:
        return Response403(msg='角色已存在')
    if len(menu.menu_id) < 1:
        raise HTTPException(status_code=403, detail='必须至少选择一个菜单')
    if len(menu.menu_id) == 1:
        if not menu_crud.get_one_menu_by_id(db, menu.menu_id[0]):
            raise HTTPException(status_code=404, detail=f'所选菜单 {menu.menu_id[0]} 不存在')
    elif len(menu.menu_id) > 1:
        for _ in menu.menu_id:
            if not menu_crud.get_one_menu_by_id(db, _):
                raise HTTPException(status_code=404, detail=f'所选菜单 {_} 不存在')
    data = role_crud.create_role(db, obj, menu)
    return Response200(data={'role': data, 'menu': menu.menu_id})


@role.put('/put/{id}', summary='修改角色', dependencies=[Depends(rbac.verify_rbac)])
def create_depm(obj: RoleUpdate, menu: RoleMenuCreate, id: int = Query(...), db: Session = Depends(get_db)):
    check = role_crud.get_one_role_by_id(db, id)
    if not check:
        return Response404(data=obj)
    check_name = role_crud.get_one_role_by_name(db, obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='角色已存在, 请更换角色名称')
    if len(menu.menu_id) < 1:
        raise HTTPException(status_code=403, detail='必须至少选择一个菜单')
    if len(menu.menu_id) == 1:
        if not menu_crud.get_one_menu_by_id(db, menu.menu_id[0]):
            raise HTTPException(status_code=404, detail=f'所选菜单 {menu.menu_id[0]} 不存在')
    elif len(menu.menu_id) > 1:
        for _ in menu.menu_id:
            if not menu_crud.get_one_menu_by_id(db, _):
                raise HTTPException(status_code=404, detail=f'所选菜单 {_} 不存在')
    data = role_crud.update_role(db, id, obj, menu)
    return Response200(data={'role': data, 'menu': menu.menu_id})


@role.delete('/delete/{id}', summary='删除角色', dependencies=[Depends(rbac.verify_rbac)])
def get_depm(id: int = Query(...), db: Session = Depends(get_db)):
    check = role_crud.get_one_role_by_id(db, id)
    if not check:
        return Response404()
    role_crud.delete_role(db, id)
    return Response200()