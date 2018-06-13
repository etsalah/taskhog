#!/usr/bin/env python
"""This model defines the users that are attached to a particular board"""
from models.common import CommonField


class BoardUser(CommonField):
    __tablename__ = "board_user"
    board_id = ""
    user_id = ""
