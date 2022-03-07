#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from redis import Redis, TimeoutError, AuthenticationError

from backend.app.common.log import log
from backend.app.core.conf import settings


# class RedisCli(object):
#
#     def __init__(self, *, host: str, port: int, password: str, db: int, socket_timeout: int = 5):
#         # redis对象 在 @app.on_event("startup") 中连接创建
#         self._redis_client = None
#         self.host = host
#         self.port = port
#         self.password = password
#         self.db = db
#         self.socket_timeout = socket_timeout
#
#     async def init_redis_connect(self) -> None:
#         """
#         初始化连接
#         :return:
#         """
#         try:
#             self._redis_client = Redis(
#                 host=self.host,
#                 port=self.port,
#                 password=self.password,
#                 db=self.db,
#                 socket_timeout=self.socket_timeout,
#                 decode_responses=True  # 解码
#             )
#             await self._redis_client.ping()
#         except TimeoutError:
#             log.error("连接redis超时")
#             sys.exit()
#         except AuthenticationError:
#             log.error("连接redis认证失败")
#             sys.exit()
#         except Exception as e:
#             log.error('连接redis异常 {}', e)
#             sys.exit()
#
#     # 使实例化后的对象 赋予redis对象的的方法和属性
#     def __getattr__(self, name):
#         return getattr(self._redis_client, name)
#
#     def __getitem__(self, name):
#         return self._redis_client[name]
#
#     def __setitem__(self, name, value):
#         self._redis_client[name] = value
#
#     def __delitem__(self, name):
#         del self._redis_client[name]
#
#
# # 创建redis连接对象
# redis_client = RedisCli(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     password=settings.REDIS_PASSWORD,
#     db=settings.REDIS_DATABASE,
#     socket_timeout=settings.REDIS_TIMEOUT
# )
#
# # 只允许导出 redis_client 实例化对象
# __all__ = ["redis_client"]

"""
 上面的方式是没有语法提示的，这里直接改用Redis, 通过源码可以得知 Redis() 是用连接池创建的
 同样在 @app.on_event("startup") 中初始化连接池
"""
try:
    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DATABASE,
        socket_timeout=settings.REDIS_TIMEOUT,
        decode_responses=True  # 解码
    )
except TimeoutError:
    log.error("连接redis超时")
    sys.exit()
except AuthenticationError:
    log.error("连接redis认证失败")
    sys.exit()
except Exception as e:
    log.error('连接redis异常 {}', e)
    sys.exit()
