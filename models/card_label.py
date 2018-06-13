#!/usr/bin/env python
"""This model defines contains the details of the board labels that are
attached to a specific card"""
from models.common import CommonField


class CardLabel(CommonField):
    __tablename__ = "card_label"
    board_label_id = ""
    card_id = ""
