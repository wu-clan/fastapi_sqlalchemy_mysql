#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from backend.app.crud.base import CRUDBase
from backend.app.models import Department
from backend.app.schemas.sm_department import DepmCreate, DepmUpdate


class DepmCRUD(CRUDBase[Department, DepmCreate, DepmUpdate]):

    def get_all_depm(self) -> Select:
        return select(Department)

    async def get_one_depm_by_name(self, db: AsyncSession, name: str) -> Department:
        data = await db.execute(select(Department).where(Department.name == name))
        return data.scalars().first()

    async def get_one_depm_by_id(self, db: AsyncSession, id: int) -> Department:
        data = await db.execute(select(Department).where(Department.id == id))
        return data.scalars().first()

    async def create_depm(self, db: AsyncSession, obj: DepmCreate) -> Department:
        return await super().create(db, obj)

    async def update_depm(self, db: AsyncSession, id: int, obj: DepmUpdate) -> DepmUpdate:
        return await super().update_one(db, id, obj)

    async def delete_depm(self, db: AsyncSession, id: int) -> bool:
        return await super().delete_one(db, id)


depm_crud = DepmCRUD(Department)
