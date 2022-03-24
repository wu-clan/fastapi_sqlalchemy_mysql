#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field


class RBACBase(BaseModel):
    role: str = Field(..., description='角色')


class RBACCreate(RBACBase):
    path: str = Field(..., description='api路径')
    method: str = Field(..., description='请求方法')


class RBACUpdate(RBACCreate):
    pass


class RBACDelete(RBACCreate):
    pass


class RBACAll(BaseModel):
    id: int
    ptype: str
    v0: str
    v1: str
    v2: str
    v3: Optional[str] = None
    v4: Optional[str] = None
    v5: Optional[str] = None

    class Config:
        orm_mode = True
