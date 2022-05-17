#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.common.sys_redis import redis_client
from backend.app.schemas import Response200

rd = APIRouter()


@rd.post('')
async def test_redis():
    result = await redis_client.set('test', 'test')
    if result:
        return Response200(data=result)


@rd.get('')
async def get_redis():
    result = await redis_client.get('test')
    if result:
        return Response200(data=result)


@rd.delete('')
async def test_redis():
    result = await redis_client.delete('test')
    if result:
        return Response200(data=result)
