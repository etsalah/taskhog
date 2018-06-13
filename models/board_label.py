#!/usr/bin/env python
"""This model represents the labels that have been created for a particular
board"""
from models.common import CommonField


class BoardLabel(CommonField):
    __tablename__ = "board_label"
    name = ""
    colour = ""
    board_id = ""
