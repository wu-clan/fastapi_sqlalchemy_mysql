#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.sql import Select

from backend.app.crud.base import CRUDBase
from backend.app.models.menu import Menu
from backend.app.schemas.sm_menu import MenuCreate, MenuUpdate


class CRUDMenu(CRUDBase[Menu, MenuCreate, MenuUpdate]):

    async def get_all_menus(self) -> Select:
        async with self.db as session:
            data = await session.execute(select(Menu).order_by(Menu.sort))
            return data.scalars().all()

    async def get_one_menu_by_id(self, menu_id: int) -> Menu:
        async with self.db as session:
            data = await session.execute(select(Menu).where(Menu.id == menu_id))
            return data.scalars().first()

    async def get_one_menu_by_name(self, menu_name: str) -> Menu:
        async with self.db as session:
            data = await session.execute(select(Menu).where(Menu.name == menu_name))
            return data.scalars().first()

    async def create_menu(self, menu: MenuCreate) -> Menu:
        return await super().create(menu)

    async def update_menu(self, menu_id: int, menu: MenuUpdate) -> Menu:
        return await super().update_one(menu_id, menu)

    async def delete_menu(self, menu_id: int) -> Menu:
        return await super().delete_one(menu_id)


MenuDao = CRUDMenu(Menu)
