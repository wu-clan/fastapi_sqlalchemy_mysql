#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from redis import Redis, TimeoutError, AuthenticationError

from backend.app.common.log import log
from backend.app.core.conf import settings


class RedisCli:

    def __init__(self):
        self.redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True  # 转码 utf-8
        )

    def init_redis_connect(self) -> Redis:
        """
        触发初始化连接
        :return:
        """
        try:
            self.redis.ping()
        except TimeoutError:
            log.error("连接redis超时")
            sys.exit()
        except AuthenticationError:
            log.error("连接redis认证失败")
            sys.exit()
        except Exception as e:
            log.error('连接redis异常 {}', e)
            sys.exit()

        return self.redis


redis_client = RedisCli().init_redis_connect()