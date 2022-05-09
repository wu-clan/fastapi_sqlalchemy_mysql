#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import Column, Integer
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    # 自动主键id
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    __name__: str

    # 自动生成表名
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def use_uuid() -> str:
    """
    使用uuid
    :return:
    """
    return uuid.uuid4().hex
