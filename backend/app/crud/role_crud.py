#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.orm import Session, Query

from backend.app.crud.base import CRUDBase
from backend.app.model import Role
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate


class RoleCRUD(CRUDBase[Role, RoleCreate, RoleUpdate]):

    def get_all_role(self, db: Session) -> Query:
        return db.query(Role)

    def get_one_role_by_name(self, db: Session, name: str) -> Role:
        return db.query(Role).filter(Role.name == name).first()

    def get_one_role_by_id(self, db: Session, id: int) -> Role:
        return super().get(db, id)

    def create_role(self, db: Session, obj: RoleCreate) -> Role:
        return super().create(db, obj)

    def update_role(self, db: Session, id: int, obj: RoleUpdate) -> Role:
        return super().update_one(db, id, obj)

    def delete_role(self, db: Session, id: int) -> bool:
        return super().delete_one(db, id)


role_crud = RoleCRUD(Role)
