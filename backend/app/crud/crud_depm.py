#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Query, contains_eager

from backend.app.crud.base import CRUDBase
from backend.app.models import Department
from backend.app.schemas.sm_department import DepmCreate, DepmUpdate


class CRUDDepm(CRUDBase[Department, DepmCreate, DepmUpdate]):

    def get_all_depm(self) -> Query:
        return self.db.query(Department)

    def get_depm_join_user_by_id(self, id: int) -> Department:
        return self.db.query(Department).join(Department.users).options(
            contains_eager(Department.users)).filter(Department.id == id).all()

    def get_one_depm_by_name(self, name: str) -> Department:
        return self.db.query(Department).filter(Department.name == name).first()

    def get_one_depm_by_id(self, id: int) -> Department:
        return super().get(id)

    def create_depm(self, obj: DepmCreate) -> Department:
        return super().create(obj)

    def update_depm(self, id: int, obj: DepmUpdate) -> DepmUpdate:
        return super().update_one(id, obj)

    def delete_depm(self, id: int) -> Department:
        return super().delete_one(id)


crud_depm = CRUDDepm(Department)
