#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid


def get_uuid() -> str:
    """
    生成uuid
    :return: str(uuid)
    """
    return str(uuid.uuid4())
