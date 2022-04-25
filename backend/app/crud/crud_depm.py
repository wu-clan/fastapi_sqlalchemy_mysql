#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.orm import Session, Query

from backend.app.crud.base import CRUDBase
from backend.app.models import Department
from backend.app.schemas.sm_department import DepmCreate, DepmUpdate


class CRUDDepm(CRUDBase[Department, DepmCreate, DepmUpdate]):

    def get_all_depm(self, db: Session) -> Query:
        return db.query(Department)

    def get_one_depm_by_name(self, db: Session, name: str) -> bool:
        return db.query(Department).filter(Department.name == name).first()

    def get_one_depm_by_id(self, db: Session, id: int) -> Department:
        return super().get(db, id)

    def create_depm(self, db: Session, obj: DepmCreate) -> Department:
        return super().create(db, obj)

    def update_depm(self, db: Session, id: int, obj: DepmUpdate) -> DepmUpdate:
        return super().update_one(db, id, obj)

    def delete_depm(self, db: Session, id: int) -> bool:
        return super().delete_one(db, id)


crud_depm = CRUDDepm(Department)
