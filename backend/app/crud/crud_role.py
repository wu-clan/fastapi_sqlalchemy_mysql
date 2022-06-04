#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql import Select

from backend.app.crud.base import CRUDBase
from backend.app.models import Role
from backend.app.models.menu import Menu
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate, RoleMenuCreate, RoleMenuUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    def get_all_role(self) -> Select:
        return select(self.model).order_by(Role.id.desc()).options(joinedload(Role.menus))

    async def get_one_role_by_name(self, name: str) -> Role:
        data = await self.db.execute(select(Role).where(Role.name == name))
        return data.scalars().first()

    async def get_role_by_id(self, role_id: int) -> Role:
        return await super().get(role_id)

    async def create_role(self, obj: RoleCreate, menu: RoleMenuCreate) -> Role:
        new_role = Role(**obj.dict())
        if len(menu.menu_id) == 1:
            new_role.menus = [await self.db.get(Menu, menu.menu_id)]
        else:
            menu_list = []
            for _ in menu.menu_id:
                menu_list.append(await self.db.get(Menu, _))
            new_role.menus = menu_list
        self.db.add(new_role)
        await self.db.commit()
        await self.db.refresh(new_role)
        return new_role

    async def update_role(self, id: int, obj: RoleUpdate, menu: RoleMenuUpdate) -> Role:
        role = await self.db.execute(select(Role).where(Role.id == id).options(selectinload(Role.menus)))
        role = role.scalars().first()
        await self.db.execute(update(Role).where(Role.id == id).values(**obj.dict()))
        # step1 删除原有的菜单
        for _ in list(role.menus):
            role.menus.remove(_)
        # step2 添加新的菜单
        if len(menu.menu_id) == 1:
            role.menus.append(await self.db.get(Menu, menu.menu_id))
        else:
            for _ in menu.menu_id:
                role.menus.append(await self.db.get(Menu, _))
        await self.db.commit()
        return role

    async def delete_role(self, id: int) -> bool:
        return await super().delete_one(id)


crud_role = CRUDRole(Role)
