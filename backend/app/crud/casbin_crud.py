#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Query, Session

from backend.app.crud.base import CRUDBase
from backend.app.model import CasbinRule
from backend.app.schemas.sm_casbin import PolicyCreate, PolicyUpdate


class RbacCRUD(CRUDBase[CasbinRule, PolicyCreate, PolicyUpdate]):

    def get_all_rbac(self, db: Session) -> Query:
        return db.query(CasbinRule)


rbac_crud = RbacCRUD(CasbinRule)
