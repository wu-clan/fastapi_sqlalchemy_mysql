#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    api_id: int


class RoleCreate(RoleBase):
    pass


class RoleDelete(RoleBase):
    pass
