#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from backend.app.api import jwt_security
from backend.app.crud.base import CRUDBase
from backend.app.model import User, Role, Department
from backend.app.model.role import UserRole
from backend.app.schemas.sm_user import CreateUser, UpdateUser, CreateUserRole


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    def get_user_by_id(self, db: Session, user_id: int) -> User:
        return super().get(db, user_id)

    def get_user_roles(self, db: Session, user_id: int) -> list:
        user_roles = db.query(UserRole.role_id).filter(UserRole.user_id == user_id).all()
        ur_list = []
        for _ in user_roles:
            ur_list.append(_[0])
        return ur_list

    def get_userinfo(self, db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).options(joinedload(User.roles)).first()

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

    def create_user(self, db: Session, create: CreateUser, role: CreateUserRole) -> User:
        create.password = jwt_security.get_hash_password(create.password)
        new_user = User(**create.dict())
        if len(role.role_id) == 1:
            new_user.roles = [db.query(Role).get(role.role_id)]
        else:
            role_list = []
            for _ in role.role_id:
                role_list.append(db.query(Role).get(_))
            new_user.roles = role_list
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def update_userinfo(self, db: Session, current_user: User, department_id: int, username: str, email: str,
                        mobile_number: str, wechat: str, qq: str, blog_address: str, introduction: str, role: list,
                        file: str) -> User:
        userinfo = db.query(User).filter(User.id == current_user.id)
        userinfo.update(
            {'username': username, 'email': email, 'mobile_number': mobile_number, 'wechat': wechat, 'qq': qq,
             'blog_address': blog_address, 'introduction': introduction})
        # 更新部门
        depm = db.query(Department).get(department_id).id
        userinfo.update({'department_id': depm})
        # 更新角色
        # step1 先删除所有角色
        for i in list(userinfo.first().roles):
            userinfo.first().roles.remove(i)
        # step2 再添加新的角色
        if len(role[0]) < 3:
            userinfo.first().roles.append(db.query(Role).get(role))
        else:
            for _ in role[0].split(","):
                userinfo.first().roles.append(db.query(Role).get(_))
        # 更新头像
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
        return super().update_one(db, uid, {'avatar': None})

    def reset_password(self, db: Session, username: str, password: str) -> bool:
        current_user = db.query(User).filter(User.username == username)
        current_user.update({'password': jwt_security.get_hash_password(password)})
        db.commit()
        return current_user.first()

    def get_users(self) -> list:
        return select(User).order_by(User.time_joined.desc()).options(joinedload(User.roles))

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
