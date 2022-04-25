#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from backend.app.crud.base import CRUDBase
from backend.app.models import Role
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    async def get_role_by_id(self, db: AsyncSession, role_id: int) -> Role:
        return await super().get(db, role_id)

    def get_all_role(self) -> Select:
        return select(Role)

    async def get_one_role_by_name(self, db: AsyncSession, name: str) -> Role:
        data = await db.execute(select(Role).where(Role.name == name))
        return data.scalars().first()

    async def get_one_role_by_id(self, db: AsyncSession, id: int) -> Role:
        data = await db.execute(select(Role).where(Role.id == id))
        return data.scalars().first()

    async def create_role(self, db: AsyncSession, obj: RoleCreate) -> Role:
        return await super().create(db, obj)

    async def update_role(self, db: AsyncSession, id: int, obj: RoleUpdate) -> Role:
        return await super().update_one(db, id, obj)

    async def delete_role(self, db: AsyncSession, id: int) -> bool:
        return await super().delete_one(db, id)


crud_role = CRUDRole(Role)
