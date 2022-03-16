#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from email_validator import EmailNotValidError, validate_email
from faker import Faker

from backend.app.datebase.db_mysql import db_session
from backend.app.model import User, Department, Role
from backend.app.common.log import log
from backend.app.api.jwt_security import get_hash_password

db = db_session()


class InitData:
    """ 初始化数据 """

    def __init__(self):
        self.fake = Faker('zh_CN')

    @staticmethod
    async def create_department():
        """ 自动创建部门 """
        dep_obj = Department(name='test')
        db.add(dep_obj)
        await db.commit()
        await db.refresh(dep_obj)
        print(f'部门 test 创建成功')

    @staticmethod
    async def create_role():
        """ 自动创建部门 """
        dep_obj = Role(name='test')
        db.add(dep_obj)
        await db.commit()
        await db.refresh(dep_obj)
        print(f'角色 test 创建成功')

    @staticmethod
    async def create_superuser_by_yourself():
        """ 手动创建管理员账户 """
        print('请输入用户名:')
        username = input()
        print('请输入密码:')
        password = input()
        print('请输入邮箱:')
        while True:
            email = input()
            try:
                success_email = validate_email(email).email
            except EmailNotValidError:
                print('邮箱不符合规范，请重新输入：')
                continue
            new_email = success_email
            break
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=new_email,
            is_superuser=True,
            department_id=1,
            role_id=1
        )
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
        print(f'管理员用户创建成功，账号：{username}，密码：{password}')

    async def create_test_user(self):
        """ 自动创建普通test用户 """
        text = 'test'
        email = self.fake.email()
        user_obj = User(
            username=text,
            password=get_hash_password(text),
            email=email,
            is_superuser=False,
            department_id=1,
            role_id=1
        )
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
        log.info(f"普通用户创建成功，账号：{text}，密码：{text}")

    async def fake_user(self):
        """ 自动创建普通用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=False,
            department_id=1,
            role_id=1
        )
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
        log.info(f"普通用户创建成功，账号：{username}，密码：{password}")

    async def fake_no_active_user(self):
        """ 自动创建锁定普通用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_active=False,
            is_superuser=False,
            department_id=1,
            role_id=1
        )
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
        log.info(f"普通锁定用户创建成功，账号：{username}，密码：{password}")

    async def fake_superuser(self):
        """ 自动创建管理员用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=True,
            department_id=1,
            role_id=1
        )
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
        log.info(f"管理员用户创建成功，账号：{username}，密码：{password}")

    async def fake_no_active_superuser(self):
        """ 自动创建锁定管理员用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_active=False,
            is_superuser=True,
            department_id=1,
            role_id=1
        )
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
        log.info(f"管理员锁定用户创建成功，账号：{username}，密码：{password}")

    async def init_data(self):
        """ 自动创建数据 """
        log.info('----------------开始初始化数据----------------')
        await self.create_department()
        await self.create_role()
        await self.create_superuser_by_yourself()
        await self.create_test_user()
        await self.fake_user()
        await self.fake_no_active_user()
        await self.fake_superuser()
        await self.fake_no_active_superuser()
        log.info('----------------数据初始化完成----------------')
        await db.close()


if __name__ == '__main__':
    init = InitData()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init.init_data())
