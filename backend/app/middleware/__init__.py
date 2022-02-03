#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.core.conf import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from backend.app.middleware.access_middle import AccessMiddleware


def register_middleware(app) -> None:
    # 跨域
    if settings.CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    # gzip
    if settings.GZIP:
        app.add_middleware(GZipMiddleware)
    if settings.ACCESS:
        # 接口访问日志
        app.add_middleware(AccessMiddleware)
