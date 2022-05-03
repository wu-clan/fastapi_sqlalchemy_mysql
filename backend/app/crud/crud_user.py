#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Query

from backend.app.api import jwt_security
from backend.app.crud.base import CRUDBase
from backend.app.models import User
from backend.app.schemas.sm_user import CreateUser, UpdateUser


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    def get_user_by_id(self, user_id: int) -> User:
        return super().get(user_id)

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def update_user_login_time(self, username: str) -> None:
        self.db.query(User).filter(User.username == username).update({'last_login': func.now()})
        self.db.commit()

    def get_email_by_username(self, username: str) -> str:
        current = self.db.query(User).filter(User.username == username).first()
        return current.email

    def get_username_by_email(self, email: str) -> str:
        return self.db.query(User).filter(User.email == email).first().username

    def get_avatar_by_username(self, username: str) -> str:
        return self.db.query(User).filter(User.username == username).first().avatar

    def create_user(self, create: CreateUser) -> User:
        create.password = jwt_security.get_hash_password(create.password)
        new_user = User(**create.dict())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_userinfo(self, current_user: User, put: UpdateUser, file: str) -> User:
        userinfo = self.db.query(User).filter(User.id == current_user.id)
        userinfo.update(jsonable_encoder(put))
        userinfo.update({
            'avatar': file
        })
        self.db.commit()
        return userinfo.first()

    def delete_user(self, user_id: int) -> User:
        return super().delete_one(user_id)

    def check_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def delete_avatar(self, user_id: int) -> User:
        return super().update_one(user_id, {'avatar': None})

    def reset_password(self, username: str, password: str) -> User:
        current_user = self.db.query(User).filter(User.username == username)
        current_user.update({'password': jwt_security.get_hash_password(password)})
        self.db.commit()
        return current_user.first()

    def get_users(self) -> Query:
        return self.db.query(User).order_by(User.time_joined.desc())

    def get_user_is_super(self, user_id: int) -> bool:
        return self.db.query(User).filter(User.id == user_id).first().is_superuser

    def get_user_is_action(self, user_id: int) -> bool:
        return self.db.query(User).filter(User.id == user_id).first().is_active

    def super_set(self, user_id: int, no_super: bool = False, is_super: bool = True) -> bool:
        user = self.db.query(User).filter(User.id == user_id)
        super_status = user.first().is_superuser
        if super_status:
            user.update({'is_superuser': no_super})
            self.db.commit()
            return super_status
        if not super_status:
            user.update({'is_superuser': is_super})
            self.db.commit()
            return super_status

    def active_set(self, user_id: int, no_action: bool = False, is_action: bool = True) -> bool:
        user = self.db.query(User).filter(User.id == user_id)
        active_status = user.first().is_active
        if active_status:
            user.update({'is_active': no_action})
            self.db.commit()
            return active_status
        if not active_status:
            user.update({'is_active': is_action})
            self.db.commit()
            return active_status


crud_user = CRUDUser(User)
