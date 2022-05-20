#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional, List

from pydantic import BaseModel

from backend.app.schemas.sm_menu import MenuAll


class RoleBase(BaseModel):
    name: str
    description: Optional[str]


class RoleCreate(RoleBase):
    pass


class RoleMenuCreate(BaseModel):
    menu_id: List[int]


class RoleUpdate(RoleBase):
    pass


class RoleMenuUpdate(RoleMenuCreate):
    pass


class RoleAll(RoleBase):
    id: int
    menus: List[MenuAll]

    class Config:
        orm_mode = True
