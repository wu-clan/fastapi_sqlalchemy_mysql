#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session, Query

from backend.app.crud.base import CRUDBase
from backend.app.model import API
from backend.app.schemas.sm_api import APICreate, APIUpdate


class RbacCRUD(CRUDBase[API, APICreate, APIUpdate]):

    def get_all_api(self, db: Session) -> Query:
        return db.query(API)

    def get_one_api_by_path(self, db: Session, path: str) -> API:
        return db.query(API).filter(API.path == path).first()

    def get_one_api_by_id(self, db: Session, id: int) -> API:
        return db.query(API).filter(API.id == id).first()

    def create_api(self, db: Session, obj: APICreate) -> API:
        return super().create(db, obj)

    def update_api(self, db: Session, id: int, obj: APIUpdate) -> API:
        return super().update_one(db, id, obj)

    def delete_api(self, db: Session, id: int) -> bool:
        return super().delete_one(db, id)


api_crud = RbacCRUD(API)
