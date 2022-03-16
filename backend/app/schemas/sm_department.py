#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel


class DepmBase(BaseModel):
    name: str
    description: Optional[str] = None


class DepmCreate(DepmBase):
    pass


class DepmUpdate(DepmBase):
    pass


class DepmAll(DepmBase):
    id: int

    class Config:
        orm_mode = True
