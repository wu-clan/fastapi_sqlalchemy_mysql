#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field


class RBACBase(BaseModel):
    role: str = Field(..., description='角色')


class RBACCreate(RBACBase):
    path: str = Field(..., description='api路径')
    method: str = Field(..., description='请求方法')


class RBACDelete(RBACCreate):
    pass
