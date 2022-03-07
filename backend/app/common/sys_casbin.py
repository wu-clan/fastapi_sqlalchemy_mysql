#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import casbin
import casbin_sqlalchemy_adapter

from backend.app.core.path_conf import RBAC_MODEL_CONF
from backend.app.datebase.db_mysql import SQLALCHEMY_DATABASE_URL


def get_casbin_enforcer() -> casbin.Enforcer:
    """
    由于 casbin_sqlalchemy_adapter 内部使用的 SQLAlchemy 同步, 这里只能使用: mysql+pymysql
    :return:
    """
    adapter = casbin_sqlalchemy_adapter.Adapter(SQLALCHEMY_DATABASE_URL)

    e = casbin.Enforcer(RBAC_MODEL_CONF, adapter)

    return e