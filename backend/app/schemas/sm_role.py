#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: Optional[str]


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleAll(RoleBase):
    id: int

    class Config:
        orm_mode = True
