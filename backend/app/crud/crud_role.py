#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select

from backend.app.crud.base import CRUDBase
from backend.app.datebase.db_mysql import get_db
from backend.app.models import Role, Menu
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate, RoleMenuCreate, RoleMenuUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    def get_all_role(self) -> Select:
        return select(self.model).order_by(Role.id.desc()).options(joinedload(Role.menus))

    def get_one_role_by_name(self, name: str) -> Role:
        with self.db as session:
            return session.query(Role).filter(Role.name == name).first()

    def get_one_role_by_id(self, id: int) -> Role:
        return super().get(id)

    def create_role(self, obj: RoleCreate, menu: RoleMenuCreate) -> Role:
        with self.db as session:
            new_role = Role(**obj.dict())
            if len(menu.menu_id) == 1:
                new_role.menus = [session.query(Menu).get(menu.menu_id)]
            else:
                menu_list = []
                for _ in menu.menu_id:
                    menu_list.append(session.query(Menu).get(_))
                new_role.menus = menu_list
            session.add(new_role)
            session.commit()
            session.refresh(new_role)
            return new_role

    def update_role(self, id: int, obj: RoleUpdate, menu: RoleMenuUpdate) -> Role:
        with self.db as session:
            role = session.query(Role).filter(Role.id == id)
            role.update(obj.dict())
            # step1 删除原有的菜单
            for _ in list(role.first().menus):
                role.first().menus.remove(_)
            # step2 添加新的菜单
            if len(menu.menu_id) == 1:
                role.first().menus.append(session.query(Menu).get(menu.menu_id))
            else:
                for _ in menu.menu_id:
                    role.first().menus.append(session.query(Menu).get(_))
            session.commit()
            return role.first()

    def delete_role(self, id: int) -> bool:
        return super().delete_one(id)


crud_role = CRUDRole(Role)
