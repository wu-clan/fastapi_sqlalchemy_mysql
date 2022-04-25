#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.sql import Select

from backend.app.crud.base import CRUDBase
from backend.app.models import CasbinRule
from backend.app.schemas.sm_casbin import PolicyCreate, PolicyUpdate


class CRUDRbac(CRUDBase[CasbinRule, PolicyCreate, PolicyUpdate]):

    def get_all_rbac(self) -> Select:
        return select(CasbinRule)


crud_rbac = CRUDRbac(CasbinRule)
