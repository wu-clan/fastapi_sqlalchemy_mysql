#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import casbin
import casbin_sqlalchemy_adapter
from fastapi import Depends, Request

from backend.app.api.jwt_security import get_current_user
from backend.app.core.conf import settings
from backend.app.core.path_conf import RBAC_MODEL_CONF
from backend.app.model import User
from backend.app.schemas import AuthenticationError


class RBAC:

    def __init__(self):
        self._Casbin_DATABASE_URL = f'mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}?charset={settings.DB_CHARSET}'

    def get_casbin_enforcer(self) -> casbin.Enforcer:
        """
        由于 casbin_sqlalchemy_adapter 内部使用的 SQLAlchemy 同步, 这里只能使用: mysql+pymysql
        :return:
        """
        adapter = casbin_sqlalchemy_adapter.Adapter(self._Casbin_DATABASE_URL)

        enforcer = casbin.Enforcer(RBAC_MODEL_CONF, adapter)

        return enforcer

    async def verify_rbac(self, request: Request, user: User = Depends(get_current_user)):
        """
        权限校验，超级用户跳过校验，默认拥有所有权限
        :param request:
        :param user:
        :return:
        """
        role_id = user.role_id
        path = request.url.path
        method = request.method

        if user.is_superuser:
            ...
        else:
            enforcer = self.get_casbin_enforcer()
            if not enforcer.enforce(str(role_id), path, method):
                raise AuthenticationError


rbac = RBAC()
