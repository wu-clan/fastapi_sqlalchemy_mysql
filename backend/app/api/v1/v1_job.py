#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from fastapi import APIRouter, Body

from backend.app.common.log import log
from backend.app.common.sys_jobs import scheduler
from backend.app.schemas import Response200, Response404, Response403

aps = APIRouter()


def test_scheduler_write_log():
    """
    测试定时执行
    :return:
    """
    log.debug('📢📢📢 test scheduler')


@aps.get("/jobs", summary="获取所有jobs")
def get_jobs_all():
    schedules = []
    for job in scheduler.get_jobs():
        schedules.append(
            {"job_id": job.id, "func_name": job.func_ref, "func_args": job.args, "cron_model": str(job.trigger)}
        )
    return Response200(data=schedules)


@aps.get("/job/{job_id}", summary="获取指定的job")
def get_target_job(job_id: str):
    job = scheduler.get_job(job_id=job_id)
    if not job:
        return Response404(msg=f"没有 job {job_id}")
    return Response200(data=job.id)


@aps.post("/job/start", summary="启动定时任务")
def add_job_to_scheduler(job_id: str = Body(...), seconds: int = Body(default=120, gt=1)):
    res = scheduler.get_job(job_id=job_id)
    if res:
        return Response403(msg=f"job {job_id} is exist")
    scheduler_job = scheduler.add_job(test_scheduler_write_log, 'interval', seconds=seconds, id=job_id,
                                      next_run_time=datetime.now())
    return Response200(msg='success', data={"id": scheduler_job.id})


@aps.delete("/job/{job_id}", summary="移除定时任务")
def remove_schedule(job_id: str):
    res = scheduler.get_job(job_id=job_id)
    if not res:
        return Response404(msg=f"没有 job {job_id}")
    scheduler.remove_job(job_id)
    return Response200(msg='移除成功')
