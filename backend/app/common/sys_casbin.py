#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import casbin
import casbin_sqlalchemy_adapter
from fastapi import Request, Depends

from backend.app.api.jwt_security import get_current_user
from backend.app.core.path_conf import RBAC_MODEL_CONF
from backend.app.datebase.db_mysql import SQLALCHEMY_DATABASE_URL
from backend.app.models import CasbinRule, User
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

    def verify_rbac(self, request: Request, user: User = Depends(get_current_user)):
        """
        权限校验，超级用户跳过校验，默认拥有所有权限
        :param request:
        :param user:
        :return:
        """
        user_uid = user.user_uid
        path = request.url.path
        method = request.method

        if user.is_superuser:
            ...
        else:
            enforcer = self.get_casbin_enforcer()
            if not enforcer.enforce(user_uid, path, method):
                raise AuthorizationError


rbac = RBAC()
