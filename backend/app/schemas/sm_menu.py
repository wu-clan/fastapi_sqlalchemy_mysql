#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    name: str
    route_name: str
    route_path: str
    url: str
    parent_id: Optional[int]
    sort: int = Field(default=0, ge=0, description="排序")
    icon: str
    file_path: str
    is_show: bool = Field(default=True, description="是否显示")


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class MenuAll(MenuBase):
    id: int

    class Config:
        orm_mode = True
