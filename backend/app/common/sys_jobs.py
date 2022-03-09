#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tzlocal
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from backend.app.core.conf import settings

_redis_conf = {
    'host': settings.APS_REDIS_HOST,
    'port': settings.APS_REDIS_PORT,
    'password': settings.APS_REDIS_PASSWORD,
    'db': settings.APS_REDIS_DATABASE,
    'socket_timeout': settings.APS_REDIS_TIMEOUT
}

_pp = ProcessPoolExecutor(settings.APS_PP_EXECUTOR_NUM)
_tp = ThreadPoolExecutor(settings.APS_TP_EXECUTOR_NUM)

if settings.APS_TP and settings.APS_PP:
    _executors = {
        # 方式调度
        'default': _tp,
        'processpool': _pp
    }

if settings.APS_PP and not settings.APS_TP:
    _executors = {
        'default': _pp
    }

if settings.APS_TP and not settings.APS_PP:
    _executors = {
        # 方式调度
        'default': _tp
    }

_interval_task = {
    # 配置存储器
    "jobstores": {
        'default': RedisJobStore(**_redis_conf)
    },
    # 配置执行器
    "executors": _executors,
    # 创建job时的默认参数
    "job_defaults": {
        'coalesce': settings.APS_COALESCE,
        'max_instances': settings.APS_MAX_INSTANCES,
    },
    "timezone": str(tzlocal.get_localzone())
}

scheduler = BackgroundScheduler(**_interval_task)

__all__ = ['scheduler']
