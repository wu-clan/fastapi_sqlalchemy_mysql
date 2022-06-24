#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.jwt_security import get_current_user
from backend.app.common.pagination import Page
from backend.app.common.sys_casbin import rbac
from backend.app.crud.crud_menu import MenuDao
from backend.app.crud.crud_role import RoleDao
from backend.app.database.db_mysql import get_db
from backend.app.schemas import Response404, Response403, Response200
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate, RoleAll, RoleMenuCreate, RoleMenuUpdate

role = APIRouter()


@role.get('', summary='获取所有角色', response_model=Page[RoleAll], dependencies=[Depends(get_current_user)])
async def get_all_role():
    async with get_db() as session:
        return await paginate(session, RoleDao.get_all_role())


@role.post('', summary='创建角色', dependencies=[Depends(rbac.verify_rbac)])
async def create_role(obj_role: RoleCreate, obj_menu: RoleMenuCreate):
    check = await RoleDao.get_one_role_by_name(obj_role.name)
    if check:
        return Response403(msg='角色已存在')
    if len(obj_menu.menu_id) < 1:
        return Response403(msg='必须至少选择一个菜单')
    if len(obj_menu.menu_id) == 1:
        if not await MenuDao.get_one_menu_by_id(obj_menu.menu_id[0]):
            return Response404(msg=f'所选菜单 {obj_menu.menu_id[0]} 不存在')
    elif len(obj_menu.menu_id) > 1:
        for _ in obj_menu.menu_id:
            if not await MenuDao.get_one_menu_by_id(_):
                return Response404(msg=f'所选菜单 {_} 不存在')
    data = await RoleDao.create_role(obj_role, obj_menu)
    return Response200(data=data)


@role.put('/{id}', summary='修改角色', dependencies=[Depends(rbac.verify_rbac)])
async def update_role(obj_role: RoleUpdate, obj_menu: RoleMenuUpdate, id: int = Query(...)):
    check = await RoleDao.get_role_by_id(id)
    if not check:
        return Response404(data=obj_role)
    check_name = await RoleDao.get_one_role_by_name(obj_role.name)
    if obj_role.name != check.name:
        if check_name:
            return Response403(msg='角色已存在, 请更换角色名称')
    if len(obj_menu.menu_id) < 1:
        return Response403(msg='必须至少选择一个菜单')
    if len(obj_menu.menu_id) == 1:
        if not await MenuDao.get_one_menu_by_id(obj_menu.menu_id[0]):
            return Response404(msg=f'所选菜单 {obj_menu.menu_id[0]} 不存在')
    elif len(obj_menu.menu_id) > 1:
        for _ in obj_menu.menu_id:
            if not await MenuDao.get_one_menu_by_id(_):
                return Response404(msg=f'所选菜单 {_} 不存在')
    data = await RoleDao.update_role(id, obj_role, obj_menu)
    return Response200(data={'role': data, 'menu': obj_menu.menu_id})


@role.delete('/{id}', summary='删除角色', dependencies=[Depends(rbac.verify_rbac)])
async def delete_role(id: int = Query(...)):
    check = await RoleDao.get_role_by_id(id)
    if not check:
        return Response404()
    await RoleDao.delete_role(id)
    return Response200()
