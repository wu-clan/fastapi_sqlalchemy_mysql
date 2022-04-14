#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from decimal import Decimal


def query_set_to_dict(obj) -> dict:
    """
    Serialize SQLAlchemy Query Set to dict
    :param obj: SQLAlchemy Query Set
    :return:
    """
    obj_dict = {}
    for column in obj.__table__.columns.keys():
        val = getattr(obj, column)
        if isinstance(val, Decimal):
            val = float(val)
        obj_dict[column] = val
    return obj_dict


def query_set_to_list(obj) -> list:
    """
    Serialize SQLAlchemy Query Set to list
    :param obj: SQLAlchemy Query Set
    :return:
    """
    ret_list = []
    for obj in obj:
        ret_dict = query_set_to_dict(obj)
        ret_list.append(ret_dict)
    return ret_list


def query_to_json(obj) -> dict:
    """
    Serialize SQLAlchemy Query Set to json
    :param obj: SQLAlchemy Query Set
    :return:
    """
    dict = obj.__dict__
    if "_sa_instance_state" in dict:
        del dict["_sa_instance_state"]
        return dict
