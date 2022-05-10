#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import func, select, update, desc
from sqlalchemy.sql import Select

from backend.app.api import jwt_security
from backend.app.crud.base import CRUDBase
from backend.app.models import User
from backend.app.schemas.sm_user import CreateUser, UpdateUser


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    async def get_user_by_id(self, user_id: int) -> User:
        return await super().get(user_id)

    async def get_user_by_username(self, username: str) -> User:
        user = await self.db.execute(select(User).where(User.username == username))
        return user.scalars().first()

    async def update_user_login_time(self, username: str) -> None:
        user = await self.db.execute(select(User).where(User.username == username))
        u = user.scalars().first()
        u.last_login = func.now()
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

    async def create_user(self, create: CreateUser) -> User:
        create.password = jwt_security.get_hash_password(create.password)
        new_user = User(**create.dict())
        self.db.add(new_user)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def update_userinfo(self, current_user: User, username: str, email: str, mobile_number: str,
                              wechat: str, qq: str, blog_address: str, introduction: str, file: str) -> User:
        user = await self.db.execute(select(User).where(User.username == current_user.username))
        await self.db.execute(update(User).where(User.id == current_user.id).values({
            'username': username, 'email': email, 'mobile_number': mobile_number, 'wechat': wechat, 'qq': qq,
            'blog_address': blog_address, 'introduction': introduction
        }))
        await self.db.execute(update(User).where(User.id == current_user.id).values({'avatar': file}))
        await self.db.commit()
        return user.scalars().first()

    async def delete_user(self, user_id: int) -> bool:
        return await super().delete_one(user_id)

    async def check_email(self, email: str) -> User:
        mail = await self.db.execute(select(User).where(User.email == email))
        return mail.scalars().first()

    async def delete_avatar(self, user_id: int) -> User:
        user = await self.db.execute(select(User).where(User.username == user_id))
        await self.db.execute(update(User).where(User.id == user_id).values({'avatar': None}))
        await self.db.commit()
        return user.scalars().first()

    async def reset_password(self, username: str, password: str) -> User:
        user = await self.db.execute(select(User).where(User.username == username))
        await self.db.execute(
            update(User).where(User.username == username).values(
                {'password': jwt_security.get_hash_password(password)}))
        await self.db.commit()
        return user.scalars().first()

    def get_users(self) -> Select:
        return select(self.model).order_by(desc(User.time_joined))

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
            await self.db.execute(update(User).where(User.id == user_id).values({'is_superuser': no_super}))
            await self.db.commit()
            return super_status
        if not super_status:
            await self.db.execute(update(User).where(User.id == user_id).values({'is_superuser': is_super}))
            await self.db.commit()
            return super_status

    async def active_set(self, user_id: int, no_action: bool = False, is_action: bool = True) -> bool:
        user = await self.db.execute(select(User).where(User.id == user_id))
        active_status = user.scalars().first().is_active
        if active_status:
            await self.db.execute(update(User).where(User.id == user_id).values({'is_active': no_action}))
            await self.db.commit()
            return active_status
        if not active_status:
            await self.db.execute(update(User).where(User.id == user_id).values({'is_active': is_action}))
            await self.db.commit()
            return active_status


crud_user = CRUDUser(User)
