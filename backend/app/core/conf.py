#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import secrets
from functools import lru_cache
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """ 配置类 """
    # FastAPI
    TITLE: str = 'FastAPI'
    VERSION: str = 'v0.0.1'
    DESCRIPTION: str = """
fastapi_mysql_demo. 🚀
    
### 点击跳转 -> [sync-Plus](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/sync-Plus)
    """
    DOCS_URL: str = '/v1/docs'
    REDOCS_URL: bool = False
    OPENAPI_URL: str = '/v1/openapi'

    # Uvicorn
    HOST: str = '127.0.0.1'
    PORT: int = 8000
    RELOAD: bool = True

    # DEBUG
    STATIC_FILES = True

    # DB
    DB_ECHO: bool = False
    DB_HOST: str = '127.0.0.1'
    DB_PORT: int = 3306
    DB_USER: str = 'root'
    DB_PASSWORD: str = '123456'
    DB_DATABASE: str = 'fm'
    DB_CHARSET: str = 'utf8mb4'

    # redis
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ''
    REDIS_DATABASE: int = 0
    REDIS_TIMEOUT: int = 5

    # APScheduler DB
    APS_REDIS_HOST: str = '127.0.0.1'
    APS_REDIS_PORT: int = 6379
    APS_REDIS_PASSWORD: str = ''
    APS_REDIS_DATABASE: int = 1
    APS_REDIS_TIMEOUT: int = 10

    # APScheduler Executor (TP:线程，PP:进程)
    APS_TP: bool = True
    APS_TP_EXECUTOR_NUM: int = 10  # 执行数 > 0
    APS_PP: bool = True
    APS_PP_EXECUTOR_NUM: int = 10  # 执行数 > 0

    # APScheduler Default
    APS_COALESCE: bool = False  # 是否合并运行
    APS_MAX_INSTANCES: int = 3  # 最大实例数

    # Captcha
    CAPTCHA_EXPIRATION_TIME: int = 60  # 单位：s

    # Casbin
    CASBIN_MODEL_NAME: str = 'rbac_model.conf'

    # Token
    ALGORITHM: str = 'HS256'  # 算法
    SECRET_KEY: str = '1VkVF75nsNABBjK_7-qz7GtzNy3AMvktc9TCPwKczCk'  # 密钥 (py生成方法：print(secrets.token_urlsafe(32)))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # token 时效 60 * 24 * 1 = 1 天

    # Email
    EMAIL_DESCRIPTION: str = 'fastapi-mysql-demo'  # 默认发件说明
    EMAIL_SERVER: str = 'smtp.qq.com'
    EMAIL_USER: str = 'xxxx-nav@qq.com'
    EMAIL_PASSWORD: str = 'cvszjyenrlvfkeaef'  # 授权密码，非邮箱密码

    # 密码重置 cookies 过期时间
    COOKIES_MAX_AGE: int = 60 * 5  # cookies 时效 60 * 5 = 5 分钟

    # 中间件
    CORS: bool = True
    GZIP: bool = True
    ACCESS: bool = True


@lru_cache
def get_settings():
    """ 读取配置优化写法 """
    return Settings()


settings = get_settings()
