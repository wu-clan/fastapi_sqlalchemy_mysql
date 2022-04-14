#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.datebase.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        具有增删改查的默认方法的 CRUD 对象。
        **Parameters**
        * `model`: 一个 SQLAlchemy 模型类
        * `schema`: Pydantic 模型类
        """
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType:
        """
        通过id查询一条数据
        :param db: session
        :param id: 主键id
        :return:
        """
        sql = select(self.model).where(self.model.id == id)
        data = await db.execute(sql)
        return data.scalars().first()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """
        通过schema类新增一条数据
        :param db: session
        :param obj_in: Pydantic 模型类
        :return:
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType,
                     obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        通过schema类更新一条数据
        :param db: session
        :param db_obj: SQLAlchemy 模型类
        :param obj_in: Pydantic 模型类 or 对应数据库字段的字典
        :return:
        """
        for attr, value in dict(obj_in).items():
            setattr(db_obj, attr, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_one(self, db: AsyncSession, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        通过 主键id 更新一条数据
        :param db: session
        :param id: 主键id
        :param obj_in: Pydantic 模型类 or 对应数据库字段的字典
        :return:
        """
        sql = await db.execute(select(self.model).where(self.model.id == id))
        model = sql.scalars().first()
        for attr, value in dict(obj_in).items():
            setattr(model, attr, value)
        await db.commit()
        return model

    async def delete_one(self, db: AsyncSession, id: int) -> bool:
        """
        通过id删除一条数据
        :param db: session
        :param id: 主键id
        :return:
        """
        sql = delete(self.model).where(self.model.id == id)
        obj = await db.execute(sql)
        await db.commit()
        return obj
