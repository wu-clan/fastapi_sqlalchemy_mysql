#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel


class DeptBase(BaseModel):
    name: str
    description: Optional[str]


class DeptCreate(DeptBase):
    pass


class DeptUpdate(DeptBase):
    pass


class DeptAll(DeptBase):
    id: int

    class Config:
        orm_mode = True
