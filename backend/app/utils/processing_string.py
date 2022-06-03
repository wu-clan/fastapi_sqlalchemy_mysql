#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def check_string(pattern, text) -> bool:
    result = re.search(pattern, text)
    if result:
        return True
    else:
        return False


def is_mobile(text: str) -> bool:
    """
    检查手机号码

    :param text:
    :return:
    """
    return check_string(r"^1[3-9]\d{9}$", text)


def is_wechat(text: str) -> bool:
    """
    检查微信号

    :param text:
    :return:
    """
    return check_string(r"^[a-zA-Z]([-_a-zA-Z0-9]{5,19})+$", text)


def is_QQ(text: str) -> bool:
    """
    检查QQ号

    :param text:
    :return:
    """
    return check_string(r"^[1-9][0-9]{4,10}$", text)
