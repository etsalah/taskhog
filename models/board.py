#!/usr/bin/env python
"""This contains the model that represents the boards in the system"""
from models.common import CommonField


class Board(CommonField):
    __tablename__ = "board"
    name = ""
    description = ""
