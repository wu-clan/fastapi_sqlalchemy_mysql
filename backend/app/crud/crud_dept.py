#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.sql import Select

from backend.app.crud.base import CRUDBase
from backend.app.models import Department
from backend.app.schemas.sm_department import DeptCreate, DeptUpdate


class CRUDDept(CRUDBase[Department, DeptCreate, DeptUpdate]):

    def get_all_dept(self) -> Select:
        return select(Department)

    async def get_one_dept_by_name(self, name: str) -> Department:
        data = await self.db.execute(select(Department).where(Department.name == name))
        return data.scalars().first()

    async def get_one_dept_by_id(self, id: int) -> Department:
        data = await self.db.execute(select(Department).where(Department.id == id))
        return data.scalars().first()

    async def create_dept(self, obj: DeptCreate) -> Department:
        return await super().create(obj)

    async def update_dept(self, id: int, obj: DeptUpdate) -> DeptUpdate:
        return await super().update_one(id, obj)

    async def delete_dept(self, id: int) -> bool:
        return await super().delete_one(id)


crud_dept = CRUDDept(Department)
