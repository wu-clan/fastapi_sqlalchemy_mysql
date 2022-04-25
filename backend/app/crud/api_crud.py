#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from backend.app.crud.base import CRUDBase
from backend.app.models import API
from backend.app.schemas.sm_api import APICreate, APIUpdate


class RbacCRUD(CRUDBase[API, APICreate, APIUpdate]):

    def get_all_api(self) -> Select:
        return select(API)

    async def get_one_api_by_name(self, db: AsyncSession, path: str) -> API:
        data = await db.execute(select(API).where(API.path == path))
        return data.scalars().first()

    async def get_one_api_by_id(self, db: AsyncSession, id: int) -> API:
        data = await db.execute(select(API).where(API.id == id))
        return data.scalars().first()

    async def create_api(self, db: AsyncSession, obj: API) -> API:
        return await super().create(db, obj)

    async def update_api(self, db: AsyncSession, id: int, obj: API) -> API:
        return await super().update_one(db, id, obj)

    async def delete_api(self, db: AsyncSession, id: int) -> bool:
        return await super().delete_one(db, id)


api_crud = RbacCRUD(API)
