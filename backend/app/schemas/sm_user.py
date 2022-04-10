#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from backend.app.schemas.sm_role import RoleAll


class Auth(BaseModel):
    username: str
    password: str


class Auth2(Auth):
    captcha: str


class CreateUser(Auth):
    department_id: int
    email: str = Field(..., example='user@example.com')


class CreateUserRole(BaseModel):
    role_id: str = Field(..., description='包含多个角色时,应该是 "1,2",而不是用list')


class UpdateUser(BaseModel):
    department_id: int
    username: str
    email: str
    mobile_number: Optional[str] = None
    wechat: Optional[str] = None
    qq: Optional[str] = None
    blog_address: Optional[str] = None
    introduction: Optional[str] = None


class UpdateUserRole(CreateUserRole):
    pass


class GetUserInfo(UpdateUser):
    id: int
    user_uid: str
    avatar: Optional[str] = None
    time_joined: Optional[datetime.datetime] = None
    last_login: Optional[datetime.datetime] = None
    is_superuser: bool
    is_active: bool
    roles: List[RoleAll]

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):
    code: str
    password1: str
    password2: str
