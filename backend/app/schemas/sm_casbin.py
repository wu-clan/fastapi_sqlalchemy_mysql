#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field


class RBACBase(BaseModel):
    sub: str = Field(..., description='用户uid或角色')


class PolicyCreate(RBACBase):
    path: str = Field(..., description='api路径')
    method: str = Field(..., description='请求方法, 必须大写')


class PolicyUpdate(PolicyCreate):
    pass


class PolicyDelete(PolicyCreate):
    pass


class UserRole(BaseModel):
    uid: str = Field(..., description='用户uid')
    role: str = Field(..., description='角色')


class RBACAll(BaseModel):
    id: int
    ptype: str
    v0: str
    v1: str
    v2: Optional[str] = None
    v3: Optional[str] = None
    v4: Optional[str] = None
    v5: Optional[str] = None

    class Config:
        orm_mode = True
