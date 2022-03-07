#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import BaseModel


class RBACBase(BaseModel):
    """
    rbac策略
    """
    sub: str


class RBACCreate(RBACBase):
    path: str
    method: str


class RBACDelete(RBACCreate):
    pass
