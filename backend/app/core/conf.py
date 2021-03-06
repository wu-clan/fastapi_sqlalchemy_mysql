#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """ 配置类 """
    # FastAPI
    TITLE: str = 'FastAPI'
    VERSION: str = 'v0.0.1'
    DESCRIPTION: str = """
fastapi_sqlalchemy_mysql. 🚀
    
### 点击跳转 -> [master](https://gitee.com/wu_cl/fastapi_sqlalchemy_mysql/tree/master/)
    """
    DOCS_URL: str = '/v1/docs'
    REDOCS_URL: str = None
    OPENAPI_URL: str = '/v1/openapi'

    # Uvicorn
    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 8000
    UVICORN_RELOAD: bool = True  # 如果此处为True，在 @app.on_event("startup") 时发生异常，则程序不会终止，详情：https://github.com/encode/starlette/issues/486

    # Static Server
    STATIC_FILES: bool = True

    # DB
    DB_ECHO: bool = False
    DB_HOST: str = '127.0.0.1'
    DB_PORT: int = 3306
    DB_USER: str = 'root'
    DB_PASSWORD: str = '123456'
    DB_DATABASE: str = 'fsm'
    DB_CHARSET: str = 'utf8mb4'

    # redis
    REDIS_OPEN: bool = False  # 如果你扩展API时使用了redis,就必须开启;如果你未使用到redis,则可以选择关闭(False)
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ''
    REDIS_DATABASE: int = 0
    REDIS_TIMEOUT: int = 5

    # Token
    TOKEN_ALGORITHM: str = 'HS256'  # 算法
    TOKEN_SECRET_KEY: str = '1VkVF75nsNABBjK_7-qz7GtzNy3AMvktc9TCPwKczCk'  # 密钥 (py生成方法：print(secrets.token_urlsafe(32)))
    TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # token 时效 60 * 24 * 1 = 1 天

    # Email
    EMAIL_DESCRIPTION: str = 'fastapi_sqlalchemy_mysql'  # 默认发件说明
    EMAIL_SERVER: str = 'smtp.qq.com'
    EMAIL_PORT: int = 465
    EMAIL_USER: str = 'xxxxx-nav@qq.com'
    EMAIL_PASSWORD: str = 'lalalalalalalala'  # 授权密码，非邮箱密码
    EMAIL_SSL: bool = True

    # 邮箱登录验证码过期时间
    EMAIL_LOGIN_CODE_MAX_AGE: int = 60 * 2  # 时效 60 * 2 = 2 分钟

    # Cookies
    COOKIES_MAX_AGE: int = 60 * 5  # cookies 时效 60 * 5 = 5 分钟

    # Middleware
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_GZIP: bool = True
    MIDDLEWARE_ACCESS: bool = True


@lru_cache
def get_settings():
    """ 读取配置优化写法 """
    return Settings()


settings = get_settings()
