#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, update, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from backend.app.api import jwt_security
from backend.app.models import User
from backend.app.schemas.sm_user import CreateUser, DeleteUser, UpdateUser


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    user = await db.execute(select(User).where(User.id == user_id))
    return user.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> User:
    user = await db.execute(select(User).where(User.username == username))
    return user.scalars().first()


async def update_user_login_time(db: AsyncSession, username: str) -> None:
    user = await db.execute(select(User).where(User.username == username))
    u = user.scalars().first()
    u.last_login = func.now()
    await db.commit()


async def get_email_by_username(db: AsyncSession, username: str) -> str:
    user = await db.execute(select(User).where(User.username == username))
    return user.scalars().first().email


async def get_username_by_email(db: AsyncSession, email: str) -> str:
    user = await db.execute(select(User).where(User.email == email))
    return user.scalars().first().username


async def get_avatar_by_username(db: AsyncSession, username: str) -> str:
    user = await db.execute(select(User).where(User.username == username))
    return user.scalars().first().avatar


async def create_user(db: AsyncSession, create: CreateUser) -> User:
    create.password = jwt_security.get_hash_password(create.password)
    new_user = User(**create.dict())
    db.add(new_user)
    await db.flush()
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_userinfo(db: AsyncSession, current_user: User, put: UpdateUser, file: str) -> User:
    data = await db.execute(select(User).where(User.id == current_user.id))
    await db.execute(update(User).where(User.id == current_user.id).values(jsonable_encoder(put)))
    await db.execute(update(User).where(User.id == current_user.id).values(jsonable_encoder({
        'avatar': file
    })))
    await db.commit()
    return data.scalars().first()


async def delete_user(db: AsyncSession, user_id: DeleteUser) -> None:
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()


async def check_email(db: AsyncSession, email: str) -> User:
    mail = await db.execute(select(User).where(User.email == email))
    return mail.scalars().first()


async def delete_avatar(db: AsyncSession, user_id: int) -> User:
    data = await db.execute(select(User).where(User.id == user_id))
    await db.execute(update(User).where(User.id == user_id).values({'avatar': None}))
    await db.commit()
    return data.scalars().first()


async def reset_password(db: AsyncSession, username: str, password: str) -> User:
    data = await db.execute(select(User).where(User.username == username))
    await db.execute(
        update(User).where(User.username == username).values({'password': jwt_security.get_hash_password(password)}))
    await db.commit()
    return data.scalars().first()


def get_users() -> Select:
    return select(User).order_by(desc(User.time_joined))


async def get_user_is_super(db: AsyncSession, user_id: int) -> bool:
    user = await db.execute(select(User).where(User.id == user_id))
    return user.scalars().first().is_superuser


async def get_user_is_action(db: AsyncSession, user_id: int) -> bool:
    user = await db.execute(select(User).where(User.id == user_id))
    return user.scalars().first().is_active


async def super_set(db: AsyncSession, user_id: int, no_super: bool = False, is_super: bool = True) -> bool:
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


async def active_set(db: AsyncSession, user_id: int, no_action: bool = False, is_action: bool = True) -> bool:
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
