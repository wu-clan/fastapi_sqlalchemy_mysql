#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session

from backend.app.api.jwt_security import get_current_user
from backend.app.common.sys_casbin import rbac
from backend.app.crud.menu_crud import menu_crud
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response403, Response200, Response404
from backend.app.schemas.sm_menu import MenuCreate
from backend.app.utils.encoding_tree import list_to_tree
from backend.app.utils.serializer_query import query_set_to_list

menu = APIRouter()


@menu.get("/all", summary='获取所有菜单', response_class=ORJSONResponse, dependencies=[Depends(get_current_user)],
          description='返回树形结构的菜单列表')
def get_all(db: Session = Depends(get_db)):
    data_list = query_set_to_list(menu_crud.get_all_menus(db))
    to_tree = list_to_tree(data_list)
    return to_tree


@menu.post("/add", summary='创建菜单', dependencies=[Depends(rbac.verify_rbac)])
def create(mn: MenuCreate, db: Session = Depends(get_db)):
    check = menu_crud.get_one_menu_by_name(db, mn.name)
    if check:
        return Response403(msg='菜单已存在, 请更换菜单展示名称')
    data = menu_crud.create_menu(db, mn)
    return Response200(data=data)


@menu.put("/put/{id}", summary='更新菜单', dependencies=[Depends(rbac.verify_rbac)])
def update(mn: MenuCreate, id: int = Query(...), db: Session = Depends(get_db)):
    check = menu_crud.get_one_menu_by_id(db, id)
    if not check:
        return Response404(data=mn)
    check_name = menu_crud.get_one_menu_by_name(db, mn.name)
    if mn.name != check.name:
        if check_name:
            return Response403(msg='部门已存在, 请更换部门名称')
    menu_crud.update_menu(db, id, mn)
    return Response200(data=mn)


@menu.delete("/delete/{id}", summary='删除菜单', dependencies=[Depends(rbac.verify_rbac)])
def delete(id: int = Query(...), db: Session = Depends(get_db)):
    check = menu_crud.get_one_menu_by_id(db, id)
    if not check:
        return Response404()
    menu_crud.delete_menu(db, id)
    return Response200()
