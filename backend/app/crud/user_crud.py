#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session, Query

from backend.app.api import jwt_security
from backend.app.crud.base import CRUDBase
from backend.app.model import User
from backend.app.schemas.sm_user import CreateUser, UpdateUser


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    def get_user_by_id(self, db: Session, user_id: int) -> User:
        return super().get(db, user_id)

    def get_user_by_username(self, db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()

    def update_user_login_time(self, db: Session, username: str) -> None:
        db.query(User).filter(User.username == username).update({'last_login': func.now()})
        db.commit()

    def get_email_by_username(self, db: Session, username: str) -> str:
        current = db.query(User).filter(User.username == username).first()
        return current.email

    def get_username_by_email(self, db: Session, email: str) -> str:
        return db.query(User).filter(User.email == email).first().username

    def get_avatar_by_username(self, db: Session, username: str) -> str:
        return db.query(User).filter(User.username == username).first().avatar

    def create_user(self, db: Session, create: CreateUser) -> User:
        create.password = jwt_security.get_hash_password(create.password)
        new_user = User(**create.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def update_userinfo(self, db: Session, current_user: User, put: UpdateUser, file: str) -> bool:
        userinfo = db.query(User).filter(User.id == current_user.id)
        userinfo.update(jsonable_encoder(put))
        userinfo.update({
            'avatar': file
        })
        db.commit()
        return userinfo.first()

    def delete_user(self, db: Session, user_id: int) -> None:
        return super().delete_one(db, user_id)

    def check_email(self, db: Session, email: str) -> bool:
        return db.query(User).filter(User.email == email).first()

    def delete_avatar(self, db: Session, uid: int) -> bool:
        user = db.query(User).filter(User.id == uid)
        user.update({'avatar': None})
        db.commit()
        return user.first()

    def reset_password(self, db: Session, username: str, password: str) -> bool:
        current_user = db.query(User).filter(User.username == username)
        current_user.update({'password': jwt_security.get_hash_password(password)})
        db.commit()
        return current_user.first()

    def get_users(self, db: Session) -> Query:
        return db.query(User).order_by(User.time_joined.desc())

    def get_user_is_super(self, db: Session, user_id: int) -> bool:
        return db.query(User).filter(User.id == user_id).first().is_superuser

    def get_user_is_action(self, db: Session, user_id: int) -> bool:
        return db.query(User).filter(User.id == user_id).first().is_active

    def super_set(self, db: Session, user_id: int, no_super: bool = False, is_super: bool = True) -> bool:
        user = db.query(User).filter(User.id == user_id)
        super_status = user.first().is_superuser
        if super_status:
            user.update({'is_superuser': no_super})
            db.commit()
            return super_status
        if not super_status:
            user.update({'is_superuser': is_super})
            db.commit()
            return super_status

    def active_set(self, db: Session, user_id: int, no_action: bool = False, is_action: bool = True) -> bool:
        user = db.query(User).filter(User.id == user_id)
        active_status = user.first().is_active
        if active_status:
            user.update({'is_active': no_action})
            db.commit()
            return active_status
        if not active_status:
            user.update({'is_active': is_action})
            db.commit()
            return active_status


user_crud = CRUDUser(User)
