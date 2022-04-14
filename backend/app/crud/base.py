#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Dict, Generic, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.datebase.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        具有增删改查的默认方法的 CRUD 对象
        """
        self.model = model

    def get(self, db: Session, id: int) -> ModelType:
        """
        通过id查询一条数据
        :param db: session
        :param id: 主键id
        :return:
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """
        通过schema类新增一条数据
        :param db: session
        :param obj_in: Pydantic 模型类
        :return:
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        通过schema类更新一条数据
        :param db: session
        :param db_obj: SQLAlchemy 模型类
        :param obj_in: Pydantic 模型类 or 对应数据库字段的字典
        :return:
        """
        for attr, value in dict(obj_in).items():
            setattr(db_obj, attr, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_one(self, db: Session, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        通过 主键id 更新一条数据
        :param db: session
        :param id: 主键id
        :param obj_in: Pydantic 模型类 or 对应数据库字段的字典
        :return:
        """
        model = db.query(self.model).filter(self.model.id == id).first()
        for attr, value in dict(obj_in).items():
            setattr(model, attr, value)
        db.commit()
        return model

    def delete_one(self, db: Session, id: int) -> ModelType:
        """
        通过id删除一条数据
        :param db: session
        :param id: 主键id
        :return:
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
