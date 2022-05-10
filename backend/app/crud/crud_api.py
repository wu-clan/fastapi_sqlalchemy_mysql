#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.sql import Select

from backend.app.crud.base import CRUDBase
from backend.app.models import API
from backend.app.schemas.sm_api import APICreate, APIUpdate


class CRUDApi(CRUDBase[API, APICreate, APIUpdate]):

    def get_all_api(self) -> Select:
        return select(self.model)

    async def get_one_api_by_name(self, path: str) -> API:
        data = await self.db.execute(select(API).where(API.path == path))
        return data.scalars().first()

    async def get_one_api_by_id(self, id: int) -> API:
        data = await self.db.execute(select(API).where(API.id == id))
        return data.scalars().first()

    async def create_api(self, obj: APICreate) -> API:
        return await super().create(obj)

    async def update_api(self, id: int, obj: APIUpdate) -> API:
        return await super().update_one(id, obj)

    async def delete_api(self, id: int) -> bool:
        return await super().delete_one(id)


crud_api = CRUDApi(API)
