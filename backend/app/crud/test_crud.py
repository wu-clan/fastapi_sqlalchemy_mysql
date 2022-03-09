#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from backend.app.crud.base import CRUDBase
from backend.app.model import User
from backend.app.schemas.sm_user import CreateUser, UpdateUser


class TestCRUD(CRUDBase[User, CreateUser, UpdateUser]):
    """
    描述：此文件仅作为测试文件，用于补充 CRUDBase 增改操作
    """

    def create_user(self, db: Session, create: CreateUser) -> User:
        return super().create(db, create)

    def update_userinfo(self, db: Session, current_user: User, put: UpdateUser) -> User:
        return super().update(db, current_user, put)


test_crud = TestCRUD(User)
