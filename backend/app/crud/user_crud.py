#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from backend.app.api import jwt_security
from backend.app.crud.base import CRUDBase
from backend.app.model import User
from backend.app.schemas.sm_user import CreateUser, UpdateUser


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User:
        return await super().get(db, user_id)

    async def get_user_by_username(self, db: AsyncSession, username: str) -> User:
        user = await db.execute(select(User).where(User.username == username))
        return user.scalars().first()

    async def update_user_login_time(self, db: AsyncSession, username: str) -> None:
        user = await db.execute(select(User).where(User.username == username))
        u = user.scalars().first()
        u.last_login = func.now()
        await db.commit()

    async def get_email_by_username(self, db: AsyncSession, username: str) -> str:
        user = await db.execute(select(User).where(User.username == username))
        return user.scalars().first().email

    async def get_username_by_email(self, db: AsyncSession, email: str) -> str:
        user = await db.execute(select(User).where(User.email == email))
        return user.scalars().first().username

    async def get_avatar_by_username(self, db: AsyncSession, username: str) -> str:
        user = await db.execute(select(User).where(User.username == username))
        return user.scalars().first().avatar

    async def create_user(self, db: AsyncSession, create: CreateUser) -> User:
        create.password = jwt_security.get_hash_password(create.password)
        new_user = User(**create.dict())
        db.add(new_user)
        await db.flush()
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def update_userinfo(self, db: AsyncSession, current_user: User, put: UpdateUser, file: str) -> bool:
        await db.execute(update(User).where(User.id == current_user.id).values(jsonable_encoder(put)))
        await db.execute(update(User).where(User.id == current_user.id).values(jsonable_encoder({
            'avatar': file
        })))
        await db.commit()
        return True

    async def delete_user(self, db: AsyncSession, user_id: int) -> None:
        return await super().delete_one(db, user_id)

    async def check_email(self, db: AsyncSession, email: str) -> bool:
        mail = await db.execute(select(User).where(User.email == email))
        return mail.scalars().first()

    async def delete_avatar(self, db: AsyncSession, uid: int) -> bool:
        await db.execute(update(User).where(User.id == uid).values({'avatar': None}))
        await db.commit()
        return True

    async def reset_password(self, db: AsyncSession, username: str, password: str) -> bool:
        await db.execute(
            update(User).where(User.username == username).values(
                {'password': jwt_security.get_hash_password(password)}))
        await db.commit()
        return True

    def get_users(self) -> Select:
        return select(User).order_by(desc(User.time_joined))

    async def get_user_is_super(self, db: AsyncSession, user_id: int) -> bool:
        user = await db.execute(select(User).where(User.id == user_id))
        return user.scalars().first().is_superuser

    async def get_user_is_action(self, db: AsyncSession, user_id: int) -> bool:
        user = await db.execute(select(User).where(User.id == user_id))
        return user.scalars().first().is_active

    async def super_set(self, db: AsyncSession, user_id: int, no_super: bool = False, is_super: bool = True) -> bool:
        user = await db.execute(select(User).where(User.id == user_id))
        super_status = user.scalars().first().is_superuser
        if super_status:
            await db.execute(update(User).where(User.id == user_id).values({'is_superuser': no_super}))
            await db.commit()
            return super_status
        if not super_status:
            await db.execute(update(User).where(User.id == user_id).values({'is_superuser': is_super}))
            await db.commit()
            return super_status

    async def active_set(self, db: AsyncSession, user_id: int, no_action: bool = False, is_action: bool = True) -> bool:
        user = await db.execute(select(User).where(User.id == user_id))
        active_status = user.scalars().first().is_active
        if active_status:
            await db.execute(update(User).where(User.id == user_id).values({'is_active': no_action}))
            await db.commit()
            return active_status
        if not active_status:
            await db.execute(update(User).where(User.id == user_id).values({'is_active': is_action}))
            await db.commit()
            return active_status


user_crud = CRUDUser(User)
