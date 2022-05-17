#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
描述：此文件仅作为测试文件，用于补充 CRUDBase 增改操作
"""

from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException

from backend.app.api.jwt_security import get_current_user
from backend.app.crud.crud_test import crud_test
from backend.app.crud.crud_user import crud_user
from backend.app.schemas import Response200, Response500
from backend.app.schemas.sm_user import CreateUser, UpdateUser

crud = APIRouter()


@crud.post('/register', summary='仅用于测试 CRUDBase 增',
           description='仅用于测试 CRUDBase 功能，会创建明文密码，无法登录，刷新数据库，有新增数据即为测试通过')
def test_user_register(obj: CreateUser):
    username = crud_user.get_user_by_username(obj.username)
    if username:
        raise HTTPException(status_code=403, detail='该用户名已被注册~ 换一个吧')
    email = crud_user.check_email(obj.email)
    if email:
        raise HTTPException(status_code=403, detail='该邮箱已被注册~ 换一个吧')
    try:
        validate_email(obj.email).email
    except EmailNotValidError:
        raise HTTPException(status_code=403, detail='邮箱格式错误，请重新输入')
    new_user = crud_test.create_user(obj)
    if new_user:
        return Response200(msg='用户注册成功', data={
            'username': new_user.username,
            'email': new_user.email
        })
    return Response500(msg='用户注册失败')


@crud.put('/me', summary='仅用于测试 CRUDBase 改',
          description='仅用于测试 CRUDBase 功能，需要使用真实用户测试，更新后，刷新数据库，查看更新效果')
def test_update_userinfo(obj: UpdateUser, current_user=Depends(get_current_user)):
    if current_user.username == obj.username:
        pass
    else:
        username = crud_user.get_user_by_username(obj.username)
        if username:
            raise HTTPException(status_code=403, detail='该用户名已存在~ 换一个吧')
    if current_user.email == obj.email:
        pass
    else:
        _email = crud_user.check_email(obj.email)
        if _email:
            raise HTTPException(status_code=403, detail='该邮箱已存在~ 换一个吧')
        try:
            validate_email(obj.email).email
        except EmailNotValidError:
            raise HTTPException(status_code=403, detail='邮箱格式错误，请重新输入')
    crud_test.update(current_user, obj)
    return Response200(msg='用户信息更新成功', data=obj)
