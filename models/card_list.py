#!/usr/bin/env python
from models.common import CommonField
"""This defines the list that have been created under a particular card"""


class CardList(CommonField):
    __tablename__ = "card_list"
    card_id = ""
    title = ""
    done = ""
