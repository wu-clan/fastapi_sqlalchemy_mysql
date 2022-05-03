#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.app.common.log import log
from backend.app.core.conf import settings

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


async def get_db() -> AsyncSession:
    """
    获取数据库会话
    :return:
    """
    async with db_session() as session:
        return session


__all__ = ['SQLALCHEMY_DATABASE_URL', 'get_db', 'db_session']
