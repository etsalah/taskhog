#!/usr/bin/env python
"""This module contains a definition of the basic fields that all the models in
the system and the crud operation that can be performed on these models"""
# from models.user import User
from helpers import query_helper

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def model_dict(obj):
    tmp = {}

    for column in obj.COLUMNS:
        value = getattr(obj, column)
        if hasattr(value, "day") and hasattr(value, "fromordinal"):
            value = str(value)
        elif column == "password":
            continue

        tmp[column] = value

    return tmp
