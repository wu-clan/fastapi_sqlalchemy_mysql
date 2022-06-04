#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import func, select, update
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql import Select

from backend.app.api import jwt_security
from backend.app.crud.base import CRUDBase
from backend.app.models import User, Role, Department
from backend.app.models.role import UserRole
from backend.app.schemas.sm_user import CreateUser, UpdateUser, CreateUserRole


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    async def get_user_by_id(self, user_id: int) -> User:
        return await super().get(user_id)

    async def get_user_roles(self, user_id: int) -> list:
        user_roles = await self.db.execute(select(UserRole.role_id).where(UserRole.user_id == user_id))
        all_roles = user_roles.scalars().all()
        ur_list = []
        for _ in all_roles:
            ur_list.append(_)
        return ur_list

    async def get_userinfo(self, user_id: int) -> User:
        user = await self.db.execute(select(User).where(User.id == user_id).options(joinedload(User.roles)))
        return user.scalars().first()

    async def get_user_by_username(self, username: str) -> User:
        user = await self.db.execute(select(User).where(User.username == username))
        return user.scalars().first()

    async def update_user_login_time(self, user: User) -> None:
        user.last_login = func.now()
        await self.db.commit()

    async def get_email_by_username(self, username: str) -> str:
        user = await self.db.execute(select(User).where(User.username == username))
        return user.scalars().first().email

    async def get_username_by_email(self, email: str) -> str:
        user = await self.db.execute(select(User).where(User.email == email))
        return user.scalars().first().username

    async def get_avatar_by_username(self, username: str) -> str:
        user = await self.db.execute(select(User).where(User.username == username))
        return user.scalars().first().avatar

    async def create_user(self, create: CreateUser, role: CreateUserRole) -> User:
        create.password = jwt_security.get_hash_password(create.password)
        new_user = User(**create.dict())
        if len(role.role_id) == 1:
            new_user.roles = await self.db.get(Role, role.role_id)
        else:
            role_list = []
            for _ in role.role_id.split(','):
                role_list.append(await self.db.get(Role, _))
            new_user.roles = role_list
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def update_userinfo(self, current_user: User, department_id: int, username: str, email: str,
                              mobile_number: str, wechat: str, qq: str, blog_address: str, introduction: str,
                              role: list,
                              file: str) -> User:
        user = await self.db.scalars(select(User).where(User.id == current_user.id).options(selectinload(User.roles)))
        await self.db.execute(
            update(User).where(User.id == current_user.id).values(
                username=username, email=email, mobile_number=mobile_number, wechat=wechat, qq=qq,
                blog_address=blog_address, introduction=introduction
            ))
        # 更新部门
        dept = await self.db.get(Department, department_id)
        await self.db.execute(update(User).where(User.id == current_user.id).values(department_id=dept.id))
        # 更新角色
        # step1 删除用户与角色的关系
        user_role = user.first().roles
        for _ in list(user_role):
            user_role.remove(_)
        # step2 添加用户与角色的关系
        if len(role[0]) == 1:
            user_role.append(await self.db.get(Role, role))
        else:
            for _ in role[0].split(','):
                user_role.append(await self.db.get(Role, _))
        # 更新头像
        await self.db.execute(update(User).where(User.id == current_user.id).values(avatar=file))
        await self.db.commit()
        return user

    async def delete_user(self, user_id: int) -> bool:
        return await super().delete_one(user_id)

    async def check_email(self, email: str) -> User:
        mail = await self.db.execute(select(User).where(User.email == email))
        return mail.scalars().first()

    async def delete_avatar(self, user_id: int) -> User:
        user = await self.db.execute(select(User).where(User.id == user_id))
        await self.db.execute(update(User).where(User.id == user_id).values(avatar=None))
        await self.db.commit()
        return user.scalars().first()

    async def reset_password(self, username: str, password: str) -> User:
        user = await self.db.execute(select(User).where(User.username == username))
        await self.db.execute(
            update(User).where(User.username == username).values(password=jwt_security.get_hash_password(password)))
        await self.db.commit()
        return user.scalars().first()

    def get_users(self) -> Select:
        return select(self.model).order_by(User.time_joined.desc()).options(joinedload(User.roles))

    async def get_user_is_super(self, user_id: int) -> bool:
        user = await self.db.execute(select(User).where(User.id == user_id))
        return user.scalars().first().is_superuser

    async def get_user_is_action(self, user_id: int) -> bool:
        user = await self.db.execute(select(User).where(User.id == user_id))
        return user.scalars().first().is_active

    async def super_set(self, user_id: int, no_super: bool = False, is_super: bool = True) -> bool:
        user = await self.db.execute(select(User).where(User.id == user_id))
        super_status = user.scalars().first().is_superuser
        if super_status:
            await self.db.execute(update(User).where(User.id == user_id).values(is_superuser=no_super))
            await self.db.commit()
            return super_status
        if not super_status:
            await self.db.execute(update(User).where(User.id == user_id).values(is_superuser=is_super))
            await self.db.commit()
            return super_status

    async def active_set(self, user_id: int, no_action: bool = False, is_action: bool = True) -> bool:
        user = await self.db.execute(select(User).where(User.id == user_id))
        active_status = user.scalars().first().is_active
        if active_status:
            await self.db.execute(update(User).where(User.id == user_id).values(is_active=no_action))
            await self.db.commit()
            return active_status
        if not active_status:
            await self.db.execute(update(User).where(User.id == user_id).values(is_active=is_action))
            await self.db.commit()
            return active_status


crud_user = CRUDUser(User)
