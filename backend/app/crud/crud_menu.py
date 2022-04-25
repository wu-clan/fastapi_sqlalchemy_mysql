#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from backend.app.crud.base import CRUDBase
from backend.app.models import Menu
from backend.app.schemas.sm_menu import MenuBase, MenuCreate, MenuUpdate


class CRUDMenu(CRUDBase[MenuBase, MenuCreate, MenuUpdate]):

    def get_all_menus(self, db: Session) -> list:
        return db.query(Menu).order_by(Menu.sort).all()

    def get_one_menu_by_id(self, db: Session, menu_id: int) -> Menu:
        return db.query(Menu).filter(Menu.id == menu_id).first()

    def get_one_menu_by_name(self, db: Session, menu_name: str) -> Menu:
        return db.query(Menu).filter(Menu.name == menu_name).first()

    def create_menu(self, db: Session, menu: MenuCreate) -> Menu:
        db_menu = Menu(**menu.dict())
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu

    def update_menu(self, db: Session, menu_id: int, menu: MenuUpdate) -> Menu:
        return super().update_one(db, menu_id, menu)

    def delete_menu(self, db: Session, menu_id: int) -> Menu:
        return super().delete_one(db, menu_id)


crud_menu = CRUDMenu(Menu)
