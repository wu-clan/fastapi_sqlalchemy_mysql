#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os
from hashlib import sha256
from typing import Any

import aiofiles
from email_validator import EmailNotValidError, validate_email
from fast_captcha import text_captcha
from fastapi import APIRouter, Depends, File, HTTPException, Request, Response, UploadFile, BackgroundTasks, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api import jwt_security
from backend.app.api.jwt_security import create_access_token, get_current_user
from backend.app.common.log import log
from backend.app.common.pagination import Page
from backend.app.common.sys_redis import redis_client
from backend.app.core.conf import settings
from backend.app.core.path_conf import AvatarPath
from backend.app.crud.crud_dept import crud_dept
from backend.app.crud.crud_role import crud_role
from backend.app.crud.crud_user import crud_user
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response200, Response404
from backend.app.schemas.sm_token import Token
from backend.app.schemas.sm_user import CreateUser, GetUserInfo, ResetPassword, Auth, Auth2, ELCode, CreateUserRole
from backend.app.utils import processing_string
from backend.app.utils.generate_string import get_uuid
from backend.app.utils.send_email import send_email_verification_code, SEND_EMAIL_LOGIN_TEXT

user = APIRouter()

headers = {"WWW-Authenticate": "Bearer"}


@user.post('/login', summary='用户登录调试', response_model=Token,
           description='form_data登录，为直接配合swagger-ui认证使用，接口数据与json_data登录一致，自由选择，注释其一即可', )
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    current_user = await crud_user.get_user_by_username(form_data.username)
    if not current_user:
        raise HTTPException(status_code=404, detail='用户名不存在', headers=headers)
    elif not jwt_security.verity_password(form_data.password, current_user.password):
        raise HTTPException(status_code=401, detail='密码错误', headers=headers)
    elif not current_user.is_active:
        raise HTTPException(status_code=401, detail='该用户已被锁定，无法登录', headers=headers)
    # 更新登陆时间
    await crud_user.update_user_login_time(current_user)
    # 查询用户角色
    user_roles = await crud_user.get_user_roles(current_user.id)
    # 创建token
    access_token = create_access_token([current_user.id, user_roles])
    # token存放redis
    uid = current_user.user_uid
    rd_token = await redis_client.get(uid)
    if not rd_token:
        await redis_client.set(uid, access_token, settings.TOKEN_EXPIRE_MINUTES)
        token = access_token
    else:
        token = rd_token
    log.success('用户 {} 登陆成功', form_data.username)
    return Token(
        msg='success',
        access_token=token,
        token_type='Bearer',
        is_superuser=current_user.is_superuser
    )


# @user.post('/login', summary='用户登录', description='json_data登录，不能配合swagger-ui认证使用', response_model=Token)
# async def user_login(obj: Auth) -> Any:
#     current_user = await crud_user.get_user_by_username(obj.username)
#     if not current_user:
#         raise HTTPException(status_code=404, detail='用户名不存在', headers=headers)
#     elif not jwt_security.verity_password(obj.password, current_user.password):
#         raise HTTPException(status_code=401, detail='密码错误', headers=headers)
#     elif not current_user.is_active:
#         raise HTTPException(status_code=401, detail='该用户已被锁定，无法登录', headers=headers)
#     # 更新登陆时间
#     await crud_user.update_user_login_time(current_user)
#     # 查询用户角色
#     user_roles = await crud_user.get_user_roles(current_user.id)
#     # 创建token
#     access_token = create_access_token([current_user.id, user_roles])
#     # token存放redis
#     uid = current_user.user_uid
#     rd_token = await redis_client.get(uid)
#     if not rd_token:
#         await redis_client.set(uid, access_token, settings.TOKEN_EXPIRE_MINUTES)
#         token = access_token
#     else:
#         token = rd_token
#     log.success('用户 {} 登陆成功', obj.username)
#     return Token(
#         msg='success',
#         access_token=token,
#         token_type='Bearer',
#         is_superuser=current_user.is_superuser
#     )


@user.post('/login/email/captcha', summary='获取邮箱登录验证码')
async def user_login_email_captcha(request: Request, obj: ELCode, tasks: BackgroundTasks) -> Any:
    current_email = await crud_user.check_email(obj.email)
    if not current_email:
        raise HTTPException(status_code=404, detail='邮箱不存在', headers=headers)
    username = await crud_user.get_username_by_email(obj.email)
    current_user = await crud_user.get_user_by_username(username)
    if not current_user.is_active:
        raise HTTPException(status_code=401, detail='该用户已被锁定，无法登录，发送验证码失败', headers=headers)
    try:
        code = text_captcha()
        tasks.add_task(send_email_verification_code, obj.email, code, SEND_EMAIL_LOGIN_TEXT)
    except Exception as e:
        log.exception('验证码发送失败 {}', e)
        raise HTTPException(status_code=500, detail='验证码发送失败')
    else:
        uid = get_uuid()
        await redis_client.set(uid, code, settings.EMAIL_LOGIN_CODE_MAX_AGE)
        request.app.state.email_login_code = uid
    return Response200(msg='验证码发送成功')


@user.post('/login/email', summary='邮箱登录', description='邮箱登录, 需同时必须开启login账号密码登录接口', response_model=Token)
async def user_login_email(request: Request, obj: Auth2) -> Any:
    current_email = await crud_user.check_email(obj.email)
    if not current_email:
        raise HTTPException(status_code=404, detail='邮箱不存在', headers=headers)
    username = await crud_user.get_username_by_email(obj.email)
    current_user = await crud_user.get_user_by_username(username)
    if not current_user.is_active:
        raise HTTPException(status_code=401, detail='该用户已被锁定，无法登录', headers=headers)
    try:
        uid = request.app.state.email_login_code
    except Exception:
        raise HTTPException(status_code=403, detail='请先获取邮箱验证码再登陆')
    r_code = await redis_client.get(f'{uid}')
    if not r_code:
        raise HTTPException(status_code=403, detail='验证码失效，请重新获取')
    if r_code != obj.code:
        raise HTTPException(status_code=412, detail='验证码输入错误')
    # 更新登陆时间
    await crud_user.update_user_login_time(current_user)
    # 查询用户角色
    user_roles = await crud_user.get_user_roles(current_user.id)
    # 创建token
    access_token = create_access_token([current_user.id, user_roles])
    uid = current_user.user_uid
    rd_token = await redis_client.get(uid)
    if not rd_token:
        await redis_client.set(uid, access_token, settings.TOKEN_EXPIRE_MINUTES)
        token = access_token
    else:
        token = rd_token
    log.success('用户 {} 登陆成功', username)
    return Token(
        msg='success',
        access_token=token,
        token_type='Bearer',
        is_superuser=current_user.is_superuser
    )


@user.post('/logout', summary='用户退出', dependencies=[Depends(get_current_user)])
async def user_logout() -> Any:
    return Response200(msg='退出登录成功')


@user.post('/register', summary='用户注册')
async def user_register(obj_user: CreateUser, obj_role: CreateUserRole) -> Any:
    username = await crud_user.get_user_by_username(obj_user.username)
    if username:
        raise HTTPException(status_code=403, detail='该用户名已被注册~ 换一个吧')
    email = await crud_user.check_email(obj_user.email)
    if email:
        raise HTTPException(status_code=403, detail='该邮箱已被注册~ 换一个吧')
    try:
        validate_email(obj_user.email).email
    except EmailNotValidError:
        raise HTTPException(status_code=403, detail='邮箱格式错误，请重新输入')
    dept = await crud_dept.get_one_dept_by_id(obj_user.department_id)
    if not dept:
        raise HTTPException(status_code=404, detail='所选部门不存在')
    if len(obj_role.role_id) == 1:
        if not await crud_role.get_role_by_id(obj_role.role_id):
            raise HTTPException(status_code=404, detail=f'所选角色 {obj_role.role_id} 不存在')
    elif len(obj_role.role_id) > 1:
        for _ in obj_role.role_id.split(','):
            if not await crud_role.get_role_by_id(_):
                raise HTTPException(status_code=404, detail=f'所选角色 {_} 不存在')
    new_user = await crud_user.create_user(obj_user, obj_role)
    return Response200(msg='用户注册成功', data={
        'username': new_user.username,
        'email': new_user.email
    })


@user.post('/password/reset/captcha', summary='获取密码重置验证码', description='可以通过用户名或者邮箱重置密码')
async def password_reset_captcha(username_or_email: str, response: Response, tasks: BackgroundTasks) -> Any:
    code = text_captcha()
    if await crud_user.get_user_by_username(username_or_email):
        try:
            response.delete_cookie(key='fast-code')
            response.delete_cookie(key='fast-username')
            response.set_cookie(key='fast-code', value=sha256(code.encode('utf-8')).hexdigest(),
                                max_age=settings.COOKIES_MAX_AGE)
            response.set_cookie(key='fast-username', value=username_or_email, max_age=settings.COOKIES_MAX_AGE)
        except Exception as e:
            log.exception('无法发送验证码 {}', e)
            raise HTTPException(status_code=500, detail='内部错误，无法发送验证码')
        try:
            current_user_email = await crud_user.get_email_by_username(username_or_email)
            tasks.add_task(send_email_verification_code, current_user_email, code)
        except Exception as e:
            log.exception('验证码发送失败 {}', e)
            raise HTTPException(status_code=500, detail='验证码发送失败')
        return Response200(msg='验证码发送成功')
    else:
        try:
            validate_email(username_or_email).email
        except EmailNotValidError:
            raise HTTPException(status_code=404, detail='用户名不存在，请重新输入')
        email_result = await crud_user.check_email(username_or_email)
        if not email_result:
            raise HTTPException(status_code=404, detail='邮箱不存在，请重新输入~')
        try:
            response.delete_cookie(key='fast-code')
            response.delete_cookie(key='fast-username')
            response.set_cookie(key='fast-code', value=sha256(code.encode('utf-8')).hexdigest(),
                                max_age=settings.COOKIES_MAX_AGE)
            username = await crud_user.get_username_by_email(username_or_email)
            response.set_cookie(key='fast-username', value=username, max_age=settings.COOKIES_MAX_AGE)
        except Exception as e:
            log.exception('无法发送验证码 {}', e)
            raise HTTPException(status_code=500, detail='内部错误，无法发送验证码')
        try:
            tasks.add_task(send_email_verification_code, username_or_email, code)
        except Exception as e:
            log.exception('验证码发送失败 {}', e)
            raise HTTPException(status_code=500, detail='验证码发送失败')
        return Response200(msg='验证码发送成功')


@user.post('/password/reset', summary='密码重置请求')
async def password_reset(obj: ResetPassword, request: Request, response: Response) -> Any:
    pwd1 = obj.password1
    pwd2 = obj.password2
    if pwd1 != pwd2:
        raise HTTPException(status_code=403, detail='两次密码输入不一致，请重新输入~')
    if request.cookies.get('fast-username') is None:
        raise HTTPException(status_code=404, detail='验证码已失效，请重新获取验证码')
    if request.cookies.get('fast-code') != sha256(obj.code.encode('utf-8')).hexdigest():
        raise HTTPException(status_code=403, detail='验证码错误')
    if not await crud_user.reset_password(request.cookies.get('fast-username'), obj.password2):
        raise HTTPException(status_code=500, detail='内部错误，密码重置失败')
    response.delete_cookie(key='fast-code')
    response.delete_cookie(key='fast-username')
    return Response200(msg='密码重置成功')


@user.get('/password/reset/done', summary='重置密码完成')
def password_reset_done() -> Any:
    return Response200(msg='重置密码完成')


@user.get('/me', summary='查看用户信息')
async def get_userinfo(current_user=Depends(get_current_user)) -> Any:
    return Response200(msg='查看用户信息成功', data=current_user)


@user.put('/me', summary='更新用户信息')
async def update_userinfo(
        department_id: int = Form(..., title='部门id'),
        username: str = Form(..., title='用户名'),
        email: str = Form(..., title='邮箱'),
        mobile_number: str = Form(None, title='手机号'),
        wechat: str = Form(None, title='微信'),
        qq: str = Form(None, title='QQ'),
        blog_address: str = Form(None, title='博客地址'),
        introduction: str = Form(None, title='自我介绍'),
        role: list = Form(..., title='角色', description='角色列表, 务必使用角色id'),
        file: UploadFile = File(None),
        current_user=Depends(get_current_user)
) -> Any:
    if current_user.username == username:
        pass
    else:
        username = await crud_user.get_user_by_username(username)
        if username:
            raise HTTPException(status_code=403, detail='该用户名已存在~ 换一个吧')
    if current_user.email == email:
        pass
    else:
        _email = await crud_user.check_email(email)
        if _email:
            raise HTTPException(status_code=403, detail='该邮箱已存在~ 换一个吧')
        try:
            validate_email(email).email
        except EmailNotValidError:
            raise HTTPException(status_code=403, detail='邮箱格式错误，请重新输入')
    dept = await crud_dept.get_one_dept_by_id(department_id)
    if not dept:
        raise HTTPException(status_code=404, detail='所选部门不存在')
    if len(role) < 1:
        raise HTTPException(status_code=403, detail='必须至少选择一个角色')
    if len(role[0]) < 3:
        if not await crud_role.get_role_by_id(role[0]):
            raise HTTPException(status_code=404, detail=f'所选角色 {role} 不存在')
    elif len(role[0]) >= 3:
        for _ in role[0].split(","):
            if not await crud_role.get_role_by_id(_):
                raise HTTPException(status_code=404, detail=f'所选角色 {_} 不存在')
    if mobile_number is not None:
        if not processing_string.is_mobile(mobile_number):
            raise HTTPException(status_code=403, detail='手机号码格式错误')
    if wechat is not None:
        if not processing_string.is_wechat(wechat):
            raise HTTPException(status_code=403, detail='微信号码输入有误')
    if qq is not None:
        if not processing_string.is_mobile(qq):
            raise HTTPException(status_code=403, detail='QQ号码输入有误')
    current_filename = await crud_user.get_avatar_by_username(current_user.username)
    if file is not None:
        if current_filename is not None:
            try:
                os.remove(AvatarPath + current_filename)
            except Exception as e:
                log.error('用户 {} 更新头像时，原头像文件 {} 删除失败\n{}', current_user.username, current_filename, e)
        new_file = await file.read()
        if 'image' not in file.content_type:
            raise HTTPException(status_code=403, detail='图片格式错误，请重新选择图片')
        _file = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')) + '_' + file.filename
        if not os.path.exists(AvatarPath):
            os.makedirs(AvatarPath)
        async with aiofiles.open(AvatarPath + f'{_file}', 'wb') as f:
            await f.write(new_file)
    else:
        _file = current_filename
    await crud_user.update_userinfo(current_user, department_id, username, email, mobile_number, wechat, qq,
                                    blog_address, introduction, role, _file)
    return Response200(data={
        'info': {'username': username, 'email': email, 'mobile_number': mobile_number, 'wechat': wechat, 'qq': qq,
                 'blog_address': blog_address, 'introduction': introduction},
        'role': role,
        'avatar': _file
    })


@user.delete('/me/avatar', summary='删除头像文件')
async def delete_avatar(current_user=Depends(jwt_security.get_current_user)) -> Any:
    current_filename = await crud_user.get_avatar_by_username(current_user.username)
    if current_filename is not None:
        try:
            os.remove(AvatarPath + current_filename)
        except Exception as e:
            log.error('用户 {} 删除头像文件 {} 失败\n{}', current_user.username, current_filename, e)
    else:
        return Response404(msg='用户没有头像文件，请上传头像文件后再执行此操作')
    await crud_user.delete_avatar(current_user.id)
    return Response200(msg='删除用户头像成功')


@user.get('', summary='获取所有用户', response_model=Page[GetUserInfo], dependencies=[Depends(jwt_security.get_current_user)])
async def get_all_users(db: AsyncSession = Depends(get_db)) -> Any:
    return await paginate(db, crud_user.get_users())


@user.post('/{id}/super', summary='修改用户超级权限', dependencies=[Depends(jwt_security.get_current_is_superuser)])
async def super_set(id: int) -> Any:
    if await crud_user.get_user_by_id(id):
        if await crud_user.super_set(id):
            return Response200(msg=f'修改超级权限成功', data=await crud_user.get_user_is_super(id))
        return Response200(msg=f'修改超级权限成功', data=await crud_user.get_user_is_super(id))
    return Response404(msg=f'用户 {id} 不存在')


@user.post('/{id}/action', summary='修改用户状态', dependencies=[Depends(jwt_security.get_current_is_superuser)])
async def active_set(id: int) -> Any:
    if await crud_user.get_user_by_id(id):
        if await crud_user.active_set(id):
            return Response200(msg=f'修改用户状态成功', data=await crud_user.get_user_is_action(id))
        return Response200(msg=f'修改用户状态成功', data=await crud_user.get_user_is_action(id))
    return Response404(msg=f'用户 {id} 不存在')


@user.delete('/me', summary='用户注销', description='用户注销 != 用户退出，注销之后用户将从数据库删除')
async def delete_user(current_user=Depends(get_current_user)) -> Any:
    current_filename = await crud_user.get_avatar_by_username(current_user.username)
    try:
        if current_filename is not None:
            os.remove(AvatarPath + current_filename)
    except Exception as e:
        log.error(f'删除用户 {current_user.username} 头像文件:{current_filename} 失败\n{e}')
    finally:
        await crud_user.delete_user(current_user.id)
        return Response200(msg='用户注销成功')
