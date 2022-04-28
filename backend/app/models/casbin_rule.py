#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String

from backend.app.datebase.base_class import Base


class CasbinRule(Base):
    """
    复刻 casbin_sqlalchemy_adapter 中的 casbinRule model类, 使用自定义Base, 避免产生 alembic 迁移问题
    """
    __tablename__ = "sys_casbin_rule"
    ptype = Column(String(255), comment='策略类型: p 或者 g')
    v0 = Column(String(255), comment="角色名称 / 用户uuid")
    v1 = Column(String(255), comment="路由 / 角色名称")
    v2 = Column(String(255), comment="请求方法")
    v3 = Column(String(255))
    v4 = Column(String(255))
    v5 = Column(String(255))

    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ", ".join(arr)

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.id, str(self))
