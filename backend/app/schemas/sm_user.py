#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr

from backend.app.schemas.sm_role import RoleAll


class Auth(BaseModel):
    username: str
    password: str


class ELCode(BaseModel):
    email: EmailStr


class Auth2(ELCode):
    code: str


class CreateUser(Auth):
    department_id: int
    email: str = Field(..., example='user@example.com')


class CreateUserRole(BaseModel):
    role_id: List[int]


class UpdateUser(BaseModel):
    department_id: int
    username: str
    email: str
    mobile_number: Optional[str]
    wechat: Optional[str]
    qq: Optional[str]
    blog_address: Optional[str]
    introduction: Optional[str]


class UpdateUserRole(CreateUserRole):
    pass


class GetUserInfo(UpdateUser):
    id: int
    user_uid: str
    avatar: Optional[str]
    time_joined: Optional[datetime.datetime]
    last_login: Optional[datetime.datetime]
    is_superuser: bool
    is_active: bool
    roles: List[RoleAll]

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):
    code: str
    password1: str
    password2: str
