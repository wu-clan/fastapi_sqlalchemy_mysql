#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.crud.base import CRUDBase
from backend.app.model import Role, Menu
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate, RoleMenuCreate, RoleMenuUpdate


class RoleCRUD(CRUDBase[Role, RoleCreate, RoleUpdate]):

    def get_all_role(self) -> list:
        return select(Role).order_by(Role.id.desc()).options(joinedload(Role.menus))

    def get_one_role_by_name(self, db: Session, name: str) -> Role:
        return db.query(Role).filter(Role.name == name).first()

    def get_one_role_by_id(self, db: Session, id: int) -> Role:
        return super().get(db, id)

    def create_role(self, db: Session, obj: RoleCreate, menu: RoleMenuCreate) -> Role:
        new_role = Role(**obj.dict())
        if len(menu.menu_id) == 1:
            new_role.menus = [db.query(Menu).get(menu.menu_id)]
        else:
            menu_list = []
            for _ in menu.menu_id:
                menu_list.append(db.query(Menu).get(_))
            new_role.menus = menu_list
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role

    def update_role(self, db: Session, id: int, obj: RoleUpdate, menu: RoleMenuUpdate) -> Role:
        role = db.query(Role).filter(Role.id == id)
        role.update(obj.dict())
        # step1 删除原有的菜单
        for _ in list(role.first().menus):
            role.first().menus.remove(_)
        # step2 添加新的菜单
        if len(menu.menu_id) == 1:
            role.first().menus.append(db.query(Menu).get(menu.menu_id))
        else:
            for _ in menu.menu_id:
                role.first().menus.append(db.query(Menu).get(_))
        db.commit()
        return role.first()

    def delete_role(self, db: Session, id: int) -> bool:
        return super().delete_one(db, id)


role_crud = RoleCRUD(Role)
