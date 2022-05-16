#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from fastapi.responses import ORJSONResponse

from backend.app.api.jwt_security import get_current_user
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_menu import crud_menu
from backend.app.schemas import Response403, Response200, Response404
from backend.app.schemas.sm_menu import MenuCreate
from backend.app.utils.encoding_tree import list_to_tree
from backend.app.utils.serializer_query import query_set_to_list

menu = APIRouter()


@menu.get("/menus", summary='获取所有菜单', response_class=ORJSONResponse, dependencies=[Depends(get_current_user)],
          description='返回树形结构的菜单列表')
def get_all_list():
    data_list = query_set_to_list(crud_menu.get_all_menus())
    to_tree = list_to_tree(data_list)
    return to_tree


@menu.post("/menu", summary='创建菜单', dependencies=[Depends(rbac.verify_rbac)])
def create_menu(obj: MenuCreate):
    check = crud_menu.get_one_menu_by_name(obj.name)
    if check:
        return Response403(msg='菜单已存在, 请更换菜单展示名称')
    data = crud_menu.create_menu(obj)
    return Response200(data=data)


@menu.put("/menu/{id}", summary='更新菜单', dependencies=[Depends(rbac.verify_rbac)])
def update_menu(obj: MenuCreate, id: int = Query(...)):
    check = crud_menu.get_one_menu_by_id(id)
    if not check:
        return Response404(data=obj)
    check_name = crud_menu.get_one_menu_by_name(obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='部门已存在, 请更换部门名称')
    crud_menu.update_menu(id, obj)
    return Response200(data=obj)


@menu.delete("/menu/{id}", summary='删除菜单', dependencies=[Depends(rbac.verify_rbac)])
def delete_menu(id: int = Query(...)):
    check = crud_menu.get_one_menu_by_id(id)
    if not check:
        return Response404()
    crud_menu.delete_menu(id)
    return Response200()
