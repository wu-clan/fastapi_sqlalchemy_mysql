#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uvicorn
from path import Path

from backend.app.api import register_app
from backend.app.common.log import log
from backend.app.core.conf import settings

app = register_app()

if __name__ == '__main__':
    try:
        uvicorn.run(app=f'{Path(__file__).stem}:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
    except Exception as e:
        log.error(f'FastAPI start filed ❗❗❗: {e}')
    else:
        log.success('🚀🚀🚀 FastAPI start success')
