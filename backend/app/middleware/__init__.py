#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI

from backend.app.core.conf import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from backend.app.middleware.access_middle import AccessMiddleware


def register_middleware(app: FastAPI) -> None:
    # cors
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    # gzip
    if settings.MIDDLEWARE_GZIP:
        app.add_middleware(GZipMiddleware)
    # access
    if settings.MIDDLEWARE_ACCESS:
        app.add_middleware(AccessMiddleware)
