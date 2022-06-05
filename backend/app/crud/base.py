#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Dict, Generic, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select

from backend.app.datebase.base_class import Base
from backend.app.datebase.db_mysql import get_db

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        具有增删改查的默认方法的 CRUD 对象。
        """
        self.model = model

    @property
    def db(self):
        """
        获取数据库连接

        :return:
        """
        return get_db()

    async def get(self, id: int) -> ModelType:
        """
        通过id查询一条数据

        :param id: 主键id
        :return:
        """
        async with self.db as session:
            sql = select(self.model).where(self.model.id == id)
            data = await session.execute(sql)
            return data.scalars().first()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        通过schema类新增一条数据

        :param obj_in: Pydantic 模型类
        :return:
        """
        async with self.db as session:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def update(self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        通过model类更新一条数据

        :param db_obj: 数据库model类
        :param obj_in: Pydantic模型类 or 对应数据库字段的字典
        :return:
        """
        async with self.db as session:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            await session.commit()
            return db_obj

    async def update_one(self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        通过主键id更新一条数据

        :param id: 主键id
        :param obj_in: Pydantic模型类 or 对应数据库字段的字典
        :return:
        """
        async with self.db as session:
            sql = await session.execute(select(self.model).where(self.model.id == id))
            model = sql.scalars().first()
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for attr, value in update_data.items():
                setattr(model, attr, value)
            await session.commit()
            return model

    async def delete_one(self, id: int) -> ModelType:
        """
        通过id删除一条数据

        :param id: 主键id
        :return:
        """
        async with self.db as session:
            obj = await session.get(self.model, id)
            await session.delete(obj)
            await session.commit()
            return obj
