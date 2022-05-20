#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field, validator


class RBACBase(BaseModel):
    sub: str = Field(..., description='角色 / 用户uid')


class PolicyCreate(RBACBase):
    path: str = Field(..., description='api路径')
    method: str = Field(..., description='请求方法, 必须大写')

    @validator('method')
    def method_must_upper(cls, v):
        assert v.isupper(), 'method must upper'
        return v


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
    v2: Optional[str]
    v3: Optional[str]
    v4: Optional[str]
    v5: Optional[str]

    class Config:
        orm_mode = True
