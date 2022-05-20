#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import enum
from typing import Optional

from pydantic import BaseModel


class Method(str, enum.Enum):
    GET = 'GET'
    POST = 'POST'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'


class APIBase(BaseModel):
    path: str
    group: Optional[str]
    description: Optional[str]
    method: Method = Method.GET


class APICreate(APIBase):
    pass


class APIUpdate(APIBase):
    pass


class APIAll(APIBase):
    id: int
    method: str

    class Config:
        orm_mode = True
