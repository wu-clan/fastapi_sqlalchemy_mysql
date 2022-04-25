#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
描述：此文件仅作为测试文件，用于补充 CRUDBase 增改操作
"""

from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.api.jwt_security import get_current_user
from backend.app.crud.test_crud import test_crud
from backend.app.crud.user_crud import user_crud
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response200, Response500
from backend.app.schemas.sm_user import CreateUser, UpdateUser

crud = APIRouter()


@crud.post('/test_register', summary='仅用于测试 CRUDBase 增',
           description='仅用于测试 CRUDBase 功能，会创建明文密码，无法登录，刷新数据库，有新增数据即为测试通过')
def test_user_register(create: CreateUser, db: Session = Depends(get_db)):
    username = user_crud.get_user_by_username(db, create.username)
    if username:
        raise HTTPException(status_code=403, detail='该用户名已被注册~ 换一个吧')
    email = user_crud.check_email(db, create.email)
    if email:
        raise HTTPException(status_code=403, detail='该邮箱已被注册~ 换一个吧')
    try:
        validate_email(create.email).email
    except EmailNotValidError:
        raise HTTPException(status_code=403, detail='邮箱格式错误，请重新输入')
    new_user = test_crud.create_user(db, create)
    if new_user:
        return Response200(msg='用户注册成功', data={
            'username': new_user.username,
            'email': new_user.email
        })
    return Response500(msg='用户注册失败')


@crud.put('/test_update_userinfo', summary='仅用于测试 CRUDBase 改',
          description='仅用于测试 CRUDBase 功能，需要使用真实用户测试，更新后，刷新数据库，查看更新效果')
def test_update_userinfo(put: UpdateUser, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.username == put.username:
        pass
    else:
        username = user_crud.get_user_by_username(db, put.username)
        if username:
            raise HTTPException(status_code=403, detail='该用户名已存在~ 换一个吧')
    if current_user.email == put.email:
        pass
    else:
        _email = user_crud.check_email(db, put.email)
        if _email:
            raise HTTPException(status_code=403, detail='该邮箱已存在~ 换一个吧')
        try:
            validate_email(put.email).email
        except EmailNotValidError:
            raise HTTPException(status_code=403, detail='邮箱格式错误，请重新输入')
        test_crud.update(db, current_user, put)
        return Response200(msg='用户信息更新成功', data=put)
    return Response500(msg='用户信息更新失败')
