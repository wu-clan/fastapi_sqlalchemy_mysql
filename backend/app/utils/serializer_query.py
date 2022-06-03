#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from decimal import Decimal

from sqlalchemy.orm import Query


def query_set_to_dict(obj: Query) -> dict:
    """
    Serialize SQLAlchemy Query Set to dict

    :param obj:
    :return:
    """
    obj_dict = {}
    for column in obj.__table__.columns.keys():
        val = getattr(obj, column)
        if isinstance(val, Decimal):
            val = float(val)
        obj_dict[column] = val
    return obj_dict


def query_set_to_list(obj: Query) -> list:
    """
    Serialize SQLAlchemy Query Set to list

    :param obj:
    :return:
    """
    ret_list = []
    for obj in obj:
        ret_dict = query_set_to_dict(obj)
        ret_list.append(ret_dict)
    return ret_list


def query_set_to_json(obj: Query) -> dict:
    """
    Serialize SQLAlchemy Query Set to json

    :param obj:
    :return:
    """
    obj_dict = obj.__dict__
    if "_sa_instance_state" in obj_dict:
        del obj_dict["_sa_instance_state"]
        return obj_dict
