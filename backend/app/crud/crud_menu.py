#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.app.crud.base import CRUDBase
from backend.app.database.db_mysql import get_db
from backend.app.models import Menu
from backend.app.schemas.sm_menu import MenuBase, MenuCreate, MenuUpdate


class CRUDMenu(CRUDBase[MenuBase, MenuCreate, MenuUpdate]):

    def get_all_menus(self) -> list:
        with self.db as session:
            return session.query(Menu).order_by(Menu.sort).all()

    def get_one_menu_by_id(self, menu_id: int) -> Menu:
        with self.db as session:
            return session.query(Menu).filter(Menu.id == menu_id).first()

    def get_one_menu_by_name(self, menu_name: str) -> Menu:
        with self.db as session:
            return session.query(Menu).filter(Menu.name == menu_name).first()

    def create_menu(self, menu: MenuCreate) -> Menu:
        return super().create(menu)

    def update_menu(self, menu_id: int, menu: MenuUpdate) -> Menu:
        return super().update_one(menu_id, menu)

    def delete_menu(self, menu_id: int) -> Menu:
        return super().delete_one(menu_id)


MenuDao = CRUDMenu(Menu)
