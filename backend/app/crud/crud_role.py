#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.sql import Select

from backend.app.crud.base import CRUDBase
from backend.app.models import Role
from backend.app.schemas.sm_role import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    async def get_role_by_id(self, role_id: int) -> Role:
        return await super().get(role_id)

    def get_all_role(self) -> Select:
        return select(self.model)

    async def get_one_role_by_name(self, name: str) -> Role:
        data = await self.db.execute(select(Role).where(Role.name == name))
        return data.scalars().first()

    async def get_one_role_by_id(self, id: int) -> Role:
        data = await self.db.execute(select(Role).where(Role.id == id))
        return data.scalars().first()

    async def create_role(self, obj: RoleCreate) -> Role:
        return await super().create(obj)

    async def update_role(self, id: int, obj: RoleUpdate) -> Role:
        return await super().update_one(id, obj)

    async def delete_role(self, id: int) -> bool:
        return await super().delete_one(id)


crud_role = CRUDRole(Role)
