#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.models import Base

""" 
说明：SqlAlchemy
"""

SQLALCHEMY_DATABASE_URL = f'mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}?charset={settings.DB_CHARSET}'

try:
    # 数据库引擎
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DB_ECHO)
    # log.success('数据库连接成功')
except Exception as e:
    log.error('数据库链接失败 {}', e)
    sys.exit()
else:
    # 创建会话（增删改查）
    db_session = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)


@asynccontextmanager
async def get_db() -> AsyncSession:
    """
    初始化数据库上下文管理器

    Ps: https://github.com/sqlalchemy/sqlalchemy/discussions/7164

    :return:
    """
    session = async_scoped_session(db_session, current_task)
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


async def create_table():
    """
    创建数据库表
    """
    async with engine.begin() as coon:
        await coon.run_sync(Base.metadata.create_all)


__all__ = ['SQLALCHEMY_DATABASE_URL', 'get_db', 'db_session']
