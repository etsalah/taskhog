#!/usr/bin/env python
"""This module contains a definition of the basic fields that all the models in
the system and the crud operation that can be performed on these models"""
# from models.user import User
import json

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
        elif column == "current_state":
            value = json.loads(value)
        elif column == "previous_state":
            if value:
                value = json.loads(value)
        tmp[column] = value

    return tmp
