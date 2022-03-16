#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.base import CRUDBase
from backend.app.model import Role
from backend.app.schemas.sm_role import RoleCreate, RoleDelete


class RoleCRUD(CRUDBase[Role, RoleCreate, RoleDelete]):
    async def get_role_by_id(self, db: AsyncSession, role_id: int) -> Role:
        return await super().get(db, role_id)


role_crud = RoleCRUD(Role)
