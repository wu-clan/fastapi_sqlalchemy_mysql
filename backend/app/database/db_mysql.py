#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.models import Base

""" 
说明：SqlAlchemy
"""

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}?charset={settings.DB_CHARSET}'

try:
    # 数据库引擎
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DB_ECHO)
    # log.success('数据库连接成功')
except Exception as e:
    log.error('数据库链接失败 {}', e)
    sys.exit()
else:
    # 创建会话（增删改查）
    db_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextmanager
def get_db() -> Session:
    """
    获取数据库会话

    :return:
    """
    session = scoped_session(db_session)
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_table():
    """
    创建数据库表
    """
    Base.metadata.create_all(engine)


__all__ = ['SQLALCHEMY_DATABASE_URL', 'get_db', 'db_session']
