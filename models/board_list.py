#!/usr/bin/env python
"""This model defines"""
from models.common import CommonField


class BoardList(CommonField):
    __tablename__ = "board_list"
    board_id = ""
    user_id = ""
    title = ""
