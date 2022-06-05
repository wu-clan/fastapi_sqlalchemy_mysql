#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Query, contains_eager

from backend.app.crud.base import CRUDBase
from backend.app.datebase.db_mysql import get_db
from backend.app.models import Department
from backend.app.schemas.sm_department import DeptCreate, DeptUpdate


class CRUDDept(CRUDBase[Department, DeptCreate, DeptUpdate]):

    def get_all_dept(self) -> Query:
        with self.db as session:
            return session.query(Department)

    def get_dept_join_user_by_id(self, id: int) -> list:
        with self.db as session:
            return session.query(Department).join(Department.users).options(
                contains_eager(Department.users).defer('password')).filter(Department.id == id).all()

    def get_one_dept_by_name(self, name: str) -> Department:
        with self.db as session:
            return session.query(Department).filter(Department.name == name).first()

    def get_one_dept_by_id(self, id: int) -> Department:
        return super().get(id)

    def create_dept(self, obj: DeptCreate) -> Department:
        return super().create(obj)

    def update_dept(self, id: int, obj: DeptUpdate) -> DeptUpdate:
        return super().update_one(id, obj)

    def delete_dept(self, id: int) -> Department:
        return super().delete_one(id)


crud_dept = CRUDDept(Department)
