#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Auth(BaseModel):
    username: str
    password: str


class Auth2(Auth):
    captcha: str


class CreateUser(Auth):
    email: str = Field(..., example='user@example.com')


class UpdateUser(BaseModel):
    username: str
    email: str
    mobile_number: Optional[int] = None
    wechat: Optional[str] = None
    qq: Optional[str] = None
    blog_address: Optional[str] = None
    introduction: Optional[str] = None


class GetUserInfo(UpdateUser):
    id: int
    avatar: Optional[str] = None
    time_joined: datetime.datetime
    last_login: datetime.datetime
    is_superuser: bool
    is_active: bool

    class Config:
        orm_mode = True


class DeleteUser(BaseModel):
    id: int


class ResetPassword(BaseModel):
    code: str
    password1: str
    password2: str
