#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Dict, Generic, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.datebase.base_class import Base
from backend.app.datebase.db_mysql import get_db

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        具有增删改查的默认方法的 CRUD 对象
        """
        self.__model = model
        self.db: Session = get_db()

    def get(self, id: int) -> ModelType:
        """
        通过id查询一条数据
        :param id: 主键id
        :return:
        """
        return self.db.query(self.__model).filter(self.__model.id == id).first()

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        通过schema类新增一条数据
        :param obj_in: Pydantic 模型类
        :return:
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.__model(**obj_in_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        通过model类更新一条数据
        :param db_obj: 数据库模型类
        :param obj_in: Pydantic模型类 or 对应数据库字段的字典
        :return:
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.db.commit()
        return db_obj

    def update_one(self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        通过主键id更新一条数据
        :param id: 主键id
        :param obj_in: Pydantic模型类 or 对应数据库字段的字典
        :return:
        """
        model = self.db.query(self.__model).filter(self.__model.id == id).first()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for attr, value in update_data.items():
            setattr(model, attr, value)
        self.db.commit()
        return model

    def delete_one(self, id: int) -> ModelType:
        """
        通过id删除一条数据
        :param id: 主键id
        :return:
        """
        obj = self.db.query(self.__model).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj
