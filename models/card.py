#!/usr/bin/env python
"""This model defines the fields that a card on a particular board list can
have with the exception of list attached to a particular card"""
from models.common import CommonField


class Card(CommonField):
    __tablename__ = "card"
    board_list_id = ""
    description = ""
    position = ""
