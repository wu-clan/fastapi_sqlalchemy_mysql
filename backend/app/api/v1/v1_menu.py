#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from fastapi.responses import ORJSONResponse

from backend.app.api.jwt_security import get_current_user
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_menu import MenuDao
from backend.app.schemas import Response403, Response200, Response404
from backend.app.schemas.sm_menu import MenuCreate
from backend.app.utils.encoding_tree import list_to_tree
from backend.app.utils.serializer_select import select_to_list

menu = APIRouter()


@menu.get("", summary='获取所有菜单', response_class=ORJSONResponse, dependencies=[Depends(get_current_user)],
          description='返回树形结构的菜单列表')
async def get_tree_menus():
    data_list = await MenuDao.get_all_menus()
    to_tree = list_to_tree(select_to_list(data_list))
    return to_tree


@menu.post("", summary='创建菜单', dependencies=[Depends(rbac.verify_rbac)])
async def create_menu(obj: MenuCreate):
    check = await MenuDao.get_one_menu_by_name(obj.name)
    if check:
        return Response403(msg='菜单已存在, 请更换菜单展示名称')
    data = await MenuDao.create_menu(obj)
    return Response200(data=data)


@menu.put("/{id}", summary='更新菜单', dependencies=[Depends(rbac.verify_rbac)])
async def update_menu(obj: MenuCreate, id: int = Query(...)):
    check = await MenuDao.get_one_menu_by_id(id)
    if not check:
        return Response404(data=obj)
    check_name = await MenuDao.get_one_menu_by_name(obj.name)
    if obj.name != check.name:
        if check_name:
            return Response403(msg='部门已存在, 请更换部门名称')
    await MenuDao.update_menu(id, obj)
    return Response200(data=obj)


@menu.delete("/{id}", summary='删除菜单', dependencies=[Depends(rbac.verify_rbac)])
async def delete_menu(id: int = Query(...)):
    check = await MenuDao.get_one_menu_by_id(id)
    if not check:
        return Response404()
    await MenuDao.delete_menu(id)
    return Response200()
