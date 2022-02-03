#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import math
from typing import TypeVar, Generic, Sequence

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from pydantic import BaseModel

T = TypeVar("T")

"""
重写分页库： fastapi-pagination 
使用方法：example link: https://github.com/uriyyo/fastapi-pagination/tree/main/examples
"""


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(20, gt=0, le=100, description="Page size")  # 默认 20 条记录

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class Page(AbstractPage[T], Generic[T]):
    data: Sequence[T]  # 数据
    total: int  # 总数据数
    page: int  # 第n页
    size: int  # 每页数量
    next: str  # 下一页参数
    previous: str  # 上一页参数
    total_pages: int  # 总页数

    __params_type__ = Params  # 使用自定义的Params

    @classmethod
    def create(
            cls,
            data: data,
            total: int,
            params: Params,
    ) -> Page[T]:
        page = params.page
        size = params.size
        total_pages = math.ceil(total / params.size)
        next = f"?page={page + 1}&size={size}" if (page + 1) <= total_pages else "null"
        previous = f"?page={page - 1}&size={size}" if (page - 1) >= 1 else "null"

        return cls(
            data=data,
            total=total,
            page=params.page,
            size=params.size,
            next=next,
            previous=previous,
            total_pages=total_pages
        )
