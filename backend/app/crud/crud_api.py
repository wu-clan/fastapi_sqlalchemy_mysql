#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Query

from backend.app.crud.base import CRUDBase
from backend.app.models import API
from backend.app.schemas.sm_api import APICreate, APIUpdate


class CRUDApi(CRUDBase[API, APICreate, APIUpdate]):

    def get_all_api(self) -> Query:
        return self.db.query(API)

    def get_one_api_by_path(self, path: str) -> API:
        return self.db.query(API).filter(API.path == path).first()

    def get_one_api_by_id(self, id: int) -> API:
        return self.db.query(API).filter(API.id == id).first()

    def create_api(self, obj: APICreate) -> API:
        return super().create(obj)

    def update_api(self, id: int, obj: APIUpdate) -> API:
        return super().update_one(id, obj)

    def delete_api(self, id: int) -> API:
        return super().delete_one(id)


crud_api = CRUDApi(API)
