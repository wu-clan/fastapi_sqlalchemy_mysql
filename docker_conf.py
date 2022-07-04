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

 ### 点击跳转 -> [sync](https://gitee.com/wu_cl/fastapi_sqlalchemy_mysql/tree/sync/)
    """
    DOCS_URL: str = '/v1/docs'
    REDOCS_URL: bool = None
    OPENAPI_URL: str = '/v1/openapi'

    # Static Server
    STATIC_FILES = False

    # DB
    DB_ECHO: bool = False
    DB_HOST: str = 'mysql'
    DB_PORT: int = 3306
    DB_USER: str = 'root'
    DB_PASSWORD: str = '123456'
    DB_DATABASE: str = 'fsm'
    DB_CHARSET: str = 'utf8mb4'

    # Redis
    REDIS_OPEN: bool = True  # 如果你扩展API时使用了redis,就必须开启;如果你未使用到redis,则可以选择关闭(False)
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ''
    REDIS_DATABASE: int = 0
    REDIS_TIMEOUT: int = 5

    # Captcha
    CAPTCHA_EXPIRATION_TIME: int = 60  # 单位：s

    # Token
    TOKEN_ALGORITHM: str = 'HS256'  # 算法
    TOKEN_SECRET_KEY: str = '1VkVF75nsNABBjK_7-qz7GtzNy3AMvktc9TCPwKczCk'  # 密钥 (py生成方法：print(secrets.token_urlsafe(32)))
    TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # token 时效 60 * 24 * 1 = 1 天

    # Email
    EMAIL_DESCRIPTION: str = 'fastapi_sqlalchemy_mysql'  # 默认发件说明
    EMAIL_SERVER: str = 'smtp.qq.com'
    EMAIL_PORT: int = 465
    EMAIL_USER: str = 'xxxx-nav@qq.com'
    EMAIL_PASSWORD: str = 'lalalalala'  # 授权密码，非邮箱密码
    EMAIL_SSL: bool = True  # 是否使用ssl

    # Cookies
    COOKIES_MAX_AGE: int = 60 * 5  # cookies 时效 60 * 5 = 5 分钟

    # 中间件
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_GZIP: bool = True
    MIDDLEWARE_ACCESS: bool = True


@lru_cache
def get_settings():
    """ 读取配置优化写法 """
    return Settings()


settings = get_settings()
