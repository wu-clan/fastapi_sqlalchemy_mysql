#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import casbin
import casbin_sqlalchemy_adapter

from fastapi import Request, Depends
from sqlalchemy.orm import Session

from backend.app.api.jwt_security import get_current_user
from backend.app.core.path_conf import RBAC_MODEL_CONF
from backend.app.crud.role_crud import role_crud
from backend.app.datebase.db_mysql import SQLALCHEMY_DATABASE_URL, get_db
from backend.app.model import CasbinRule, User
from backend.app.schemas import AuthorizationError


class RBAC:

    @staticmethod
    def get_casbin_enforcer() -> casbin.Enforcer:
        """
        由于 casbin_sqlalchemy_adapter 内部使用的 SQLAlchemy 同步, 这里只能使用: mysql+pymysql
        :return:
        """
        adapter = casbin_sqlalchemy_adapter.Adapter(SQLALCHEMY_DATABASE_URL, db_class=CasbinRule)

        enforcer = casbin.Enforcer(RBAC_MODEL_CONF, adapter)

        return enforcer

    def verify_rbac(self, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        """
        权限校验，超级用户跳过校验，默认拥有所有权限
        :param request:
        :param user:
        :param db:
        :return:
        """
        user_id = user.user_id
        role_id = user.role_id
        path = request.url.path
        method = request.method.lower()

        if user.is_superuser:
            ...
        else:
            enforcer = self.get_casbin_enforcer()
            if len(role_id) > 1:
                for _ in role_id.split(','):
                    role = role_crud.get_one_role_by_id(db, _)  # 获取用户角色
                    if not enforcer.enforce(role.name, path, method) and not enforcer.enforce(user_id, path, method):
                        raise AuthorizationError
            else:
                role = role_crud.get_one_role_by_id(db, role_id)  # 获取用户角色
                if not enforcer.enforce(role.name, path, method) and not enforcer.enforce(user_id, path, method):
                    raise AuthorizationError


rbac = RBAC()
