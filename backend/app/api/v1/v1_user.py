#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os
from hashlib import sha256

import aiofiles
from email_validator import EmailNotValidError, validate_email
from fast_captcha import text_captcha
from fastapi import APIRouter, Depends, File, HTTPException, Request, Response, status, UploadFile, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api import jwt_security
from backend.app.api.jwt_security import create_access_token, get_current_user
from backend.app.common.log import log
from backend.app.common.pagination import Page
from backend.app.common.sys_redis import redis_client
from backend.app.core.conf import settings
from backend.app.core.path_conf import ImgPath
from backend.app.crud.crud_depm import crud_depm
from backend.app.crud.crud_role import crud_role
from backend.app.crud.crud_user import crud_user
from backend.app.datebase.db_mysql import get_db
from backend.app.schemas import Response200, Response500, Response404
from backend.app.schemas.sm_token import Token
from backend.app.schemas.sm_user import CreateUser, GetUserInfo, ResetPassword, UpdateUser, Auth, Auth2, ELCode, \
    UpdateUserRole, CreateUserRole
from backend.app.utils import process_string
from backend.app.utils.generate_string import get_uuid
from backend.app.utils.send_email import send_email_verification_code, SEND_EMAIL_LOGIN_TEXT

user = APIRouter()

headers = {"WWW-Authenticate": "Bearer"}


@user.post('/login', summary='用户登录调试', response_model=Token,
           description='form_data登录，为直接配合swagger-ui认证使用，接口数据与json_data登录一致，自由选择，注释其一即可', )
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    current_user = await crud_user.get_user_by_username(db, form_data.username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户名不存在', headers=headers)
    elif not jwt_security.verity_password(form_data.password, current_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='密码错误', headers=headers)
    elif not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='该用户已被锁定，无法登录', headers=headers)
    # 更新登陆时间
    await crud_user.update_user_login_time(db, current_user)
    # 查询用户角色
    user_roles = await crud_user.get_user_roles(db, current_user.id)
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
    return Token(code=200, msg='success', access_token=token, token_type='Bearer',
                 is_superuser=current_user.is_superuser)


# @user.post('/login', summary='用户登录', description='json_data登录，不能配合swagger-ui认证使用', response_model=Token)
# async def user_login(user_info: Auth, db: AsyncSession = Depends(get_db)):
#     current_user = await crud_user.get_user_by_username(db, user_info.username)
#     if not current_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户名不存在', headers=headers)
#     elif not jwt_security.verity_password(user_info.password, current_user.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='密码错误', headers=headers)
#     elif not current_user.is_active:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='该用户已被锁定，无法登录', headers=headers)
#     # 更新登陆时间
#     await crud_user.update_user_login_time(db, current_user)
#     # 查询用户角色
#     user_roles = await crud_user.get_user_roles(db, current_user.id)
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
#     log.success('用户 {} 登陆成功', user_info.username)
#     return Token(code=200, msg='success', access_token=token, token_type='Bearer',
#                  is_superuser=current_user.is_superuser)


@user.post('/email_login_code', summary='获取邮箱登录验证码')
async def get_email_login_code(request: Request, email: ELCode, tasks: BackgroundTasks,
                               db: AsyncSession = Depends(get_db)):
    if not await crud_user.check_email(db, email.email):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='邮箱不存在', headers=headers)
    username = await crud_user.get_username_by_email(db, email.email)
    current_user = await crud_user.get_user_by_username(db, username)
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='该用户已被锁定，无法登录，发送验证码失败', headers=headers)
    try:
        code = text_captcha()
        tasks.add_task(send_email_verification_code, email.email, code, SEND_EMAIL_LOGIN_TEXT)
    except Exception as e:
        log.exception('验证码发送失败 {}', e)
        raise HTTPException(status_code=500, detail='验证码发送失败')
    else:
        uid = get_uuid()
        await redis_client.set(uid, code, settings.EMAIL_LOGIN_CODE_MAX_AGE)
        request.app.state.email_login_code = uid
    return Response200(msg='验证码发送成功')


@user.post('/login2', summary='邮箱登录', description='邮箱登录, 需同时必须开启login账号密码登录接口', response_model=Token)
async def user_login(request: Request, email: Auth2, db: AsyncSession = Depends(get_db)):
    username = await crud_user.get_username_by_email(db, email.email)
    current_user = await crud_user.get_user_by_username(db, username)
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='该用户已被锁定，无法登录', headers=headers)
    try:
        uid = request.app.state.email_login_code
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='请先获取邮箱验证码再登陆')
    r_code = await redis_client.get(f'{uid}')
    if not r_code:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='验证码失效，请重新获取')
    if r_code != email.code:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail='验证码输入错误')
    # 更新登陆时间
    await crud_user.update_user_login_time(db, current_user)
    # 查询用户角色
    user_roles = await crud_user.get_user_roles(db, current_user.id)
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
    return Token(code=200, msg='success', access_token=token, token_type='Bearer',
                 is_superuser=current_user.is_superuser)


@user.post('/logout', summary='用户退出')
async def logout(current_user=Depends(get_current_user)):
    if current_user:
        return Response200(msg='退出登录成功')
    return Response500(msg='退出登陆失败')


@user.post('/register', summary='用户注册')
async def user_register(create: CreateUser, role: CreateUserRole, db: AsyncSession = Depends(get_db)):
    username = await crud_user.get_user_by_username(db, create.username)
    if username:
        raise HTTPException(status_code=403, detail='该用户名已被注册~ 换一个吧')
    email = await crud_user.check_email(db, create.email)
    if email:
        raise HTTPException(status_code=403, detail='该邮箱已被注册~ 换一个吧')
    try:
        validate_email(create.email).email
    except EmailNotValidError:
        raise HTTPException(status_code=403, detail='邮箱格式错误，请重新输入')
    depm = await crud_depm.get_one_depm_by_id(db, create.department_id)
    if not depm:
        raise HTTPException(status_code=404, detail='所选部门不存在')
    if len(role.role_id) == 1:
        if not await crud_role.get_one_role_by_id(db, role.role_id):
            raise HTTPException(status_code=404, detail=f'所选角色 {role.role_id} 不存在')
    elif len(role.role_id) > 1:
        for _ in role.role_id.split(','):
            if not await crud_role.get_one_role_by_id(db, _):
                raise HTTPException(status_code=404, detail=f'所选角色 {_} 不存在')
    new_user = await crud_user.create_user(db, create, role)
    if new_user:
        log.success('用户 %s 注册成功' % create.username)
        return Response200(msg='用户注册成功', data={
            'username': new_user.username,
            'email': new_user.email
        })
    log.error('用户 %s 注册失败' % create.username)
    return Response500(msg='用户注册失败')


@user.post('/password_reset_code', summary='获取密码重置验证码', description='可以通过用户名或者邮箱重置密码')
async def password_reset_code(username_or_email: str, response: Response, tasks: BackgroundTasks,
                              db: AsyncSession = Depends(get_db)):
    code = text_captcha()
    if await crud_user.get_user_by_username(db, username_or_email):
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
            current_user_email = await crud_user.get_email_by_username(db, username_or_email)
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
        email_result = await crud_user.check_email(db, username_or_email)
        if not email_result:
            raise HTTPException(status_code=404, detail='邮箱不存在，请重新输入~')
        try:
            response.delete_cookie(key='fast-code')
            response.delete_cookie(key='fast-username')
            response.set_cookie(key='fast-code', value=sha256(code.encode('utf-8')).hexdigest(),
                                max_age=settings.COOKIES_MAX_AGE)
            username = await crud_user.get_username_by_email(db, username_or_email)
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


@user.post('/password_reset_req', summary='密码重置请求')
async def password_reset(reset_pwd: ResetPassword, request: Request, response: Response,
                         db: AsyncSession = Depends(get_db)):
    pwd1 = reset_pwd.password1
    pwd2 = reset_pwd.password2
    if pwd1 != pwd2:
        raise HTTPException(status_code=403, detail='两次密码输入不一致，请重新输入~')
    if request.cookies.get('fast-username') is None:
        raise HTTPException(status_code=404, detail='cookie已失效，请重新获取验证码')
    if request.cookies.get('fast-code') != sha256(reset_pwd.code.encode('utf-8')).hexdigest():
        raise HTTPException(status_code=403, detail='验证码错误')
    if not await crud_user.reset_password(db, request.cookies.get('fast-username'), reset_pwd.password2):
        raise HTTPException(status_code=500, detail='内部错误，密码重置失败')
    response.delete_cookie(key='fast-code')
    response.delete_cookie(key='fast-username')
    return Response200(msg='密码重置成功')


@user.get('/password_reset_done', summary='重置密码完成')
def password_reset_done():
    return HTTPException(status_code=200, detail='重置密码完成')


@user.get('/userinfo', summary='查看用户信息')
async def userinfo(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user:
        if await crud_user.get_user_by_id(db, current_user.id):
            info = await crud_user.get_userinfo(db, current_user.id)
            if info:
                return Response200(msg='查看用户信息成功', data=info)
            return Response404(msg='用户不存在')


@user.put('/update_userinfo', summary='更新用户信息')
async def update_userinfo(put: UpdateUser = Depends(UpdateUser), role: UpdateUserRole = Depends(UpdateUserRole),
                          file: UploadFile = File(None), current_user=Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    if current_user.username == put.username:
        pass
    else:
        username = await crud_user.get_user_by_username(db, put.username)
        if username:
            raise HTTPException(status_code=403, detail='该用户名已存在~ 换一个吧')
    if current_user.email == put.email:
        pass
    else:
        _email = await crud_user.check_email(db, put.email)
        if _email:
            raise HTTPException(status_code=403, detail='该邮箱已存在~ 换一个吧')
        try:
            validate_email(put.email).email
        except EmailNotValidError:
            raise HTTPException(status_code=403, detail='邮箱格式错误，请重新输入')
    depm = await crud_depm.get_one_depm_by_id(db, put.department_id)
    if not depm:
        raise HTTPException(status_code=404, detail='所选部门不存在')
    if len(role.role_id) == 1:
        if not await crud_role.get_one_role_by_id(db, role.role_id):
            raise HTTPException(status_code=404, detail=f'所选角色 {role.role_id} 不存在')
    elif len(role.role_id) > 1:
        for _ in role.role_id.split(','):
            if not await crud_role.get_one_role_by_id(db, _):
                raise HTTPException(status_code=404, detail=f'所选角色 {_} 不存在')
    if put.mobile_number is not None:
        if not process_string.is_mobile(put.mobile_number):
            raise HTTPException(status_code=403, detail='手机号码格式错误')
    if put.wechat is not None:
        if not process_string.is_wechat(put.wechat):
            raise HTTPException(status_code=403, detail='微信号码输入有误')
    if put.qq is not None:
        if not process_string.is_mobile(put.qq):
            raise HTTPException(status_code=403, detail='QQ号码输入有误')
    current_filename = await crud_user.get_avatar_by_username(db, current_user.username)
    if file is not None:
        if current_filename is not None:
            try:
                os.remove(ImgPath + current_filename)
            except Exception as e:
                log.error('用户 {} 更新头像时，原头像文件 {} 删除失败\n{}', current_user.username, current_filename, e)
        new_file = await file.read()
        if 'image' not in file.content_type:
            raise HTTPException(status_code=403, detail='图片格式错误，请重新选择图片')
        _file = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')) + '_' + file.filename
        if not os.path.exists(ImgPath):
            os.makedirs(ImgPath)
        async with aiofiles.open(ImgPath + f'{_file}', 'wb') as f:
            await f.write(new_file)
    else:
        _file = current_filename
    if current_user:
        await crud_user.update_userinfo(db, current_user, put, role, _file)
        return Response200(msg='用户信息更新成功', data={'info': put, 'role': role, 'avatar': _file})
    return Response500(msg='用户信息更新失败')


@user.delete('/delete_avatar', summary='删除头像文件')
async def delete_avatar(current_user=Depends(jwt_security.get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user:
        current_filename = await crud_user.get_avatar_by_username(db, current_user.username)
        if current_filename is not None:
            try:
                os.remove(ImgPath + current_filename)
            except Exception as e:
                log.error('用户 {} 删除头像文件 {} 失败\n{}', current_user.username, current_filename, e)
        else:
            return HTTPException(status_code=404, detail='用户没有头像文件，请上传头像文件后再执行此操作')
        await crud_user.delete_avatar(db, current_user.id)
        return Response200(msg='删除用户头像成功')
    return Response500(msg='删除用户头像失败')


@user.get('/user_list', summary='获取用户列表', dependencies=[Depends(jwt_security.get_current_user)],
          response_model=Page[GetUserInfo])
async def get_user_list(db: AsyncSession = Depends(get_db)):
    user_list = await crud_user.get_users()
    return await paginate(db, user_list)


@user.post('/user_super_set/{pk}', summary='修改用户超级权限', dependencies=[Depends(jwt_security.get_current_is_superuser)])
async def super_set(pk: int, db: AsyncSession = Depends(get_db)):
    if await crud_user.get_user_by_id(db, pk):
        if await crud_user.super_set(db, pk):
            return Response200(msg=f'修改超级权限成功，当前：{await crud_user.get_user_is_super(db, pk)}')
        return Response200(msg=f'修改超级权限成功，当前：{await crud_user.get_user_is_super(db, pk)}')
    return Response404(msg=f'用户 {pk} 不存在')


@user.post('/user_action_set/{pk}', summary='修改用户状态', dependencies=[Depends(jwt_security.get_current_is_superuser)])
async def active_set(pk: int, db: AsyncSession = Depends(get_db)):
    if await crud_user.get_user_by_id(db, pk):
        if await crud_user.active_set(db, pk):
            return Response200(msg=f'修改用户状态成功, 当前：{await crud_user.get_user_is_action(db, pk)}')
        return Response200(msg=f'修改用户状态成功, 当前：{await crud_user.get_user_is_action(db, pk)}')
    return Response404(msg=f'用户 {pk} 不存在')


@user.delete('/user_delete', summary='用户注销', description='用户注销 != 用户退出，注销之后用户将从数据库删除')
async def user_delete(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        current_filename = await crud_user.get_avatar_by_username(db, current_user.username)
        os.remove(ImgPath + current_filename)
    except FileExistsError:
        pass
    finally:
        await crud_user.delete_user(db, current_user.id)
        log.info('用户 {} 已注销, 用户信息清除完成', current_user.username)
        return Response200(msg='用户注销成功')
