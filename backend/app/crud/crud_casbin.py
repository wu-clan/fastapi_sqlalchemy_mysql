#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Query, Session

from backend.app.crud.base import CRUDBase
from backend.app.models import CasbinRule
from backend.app.schemas.sm_casbin import PolicyCreate, PolicyUpdate


class CRUDRbac(CRUDBase[CasbinRule, PolicyCreate, PolicyUpdate]):

    def get_all_rbac(self, db: Session) -> Query:
        return db.query(CasbinRule)


crud_rbac = CRUDRbac(CasbinRule)
