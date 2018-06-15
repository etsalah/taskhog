#!/usr/bin/env python
"""This model defines the fields that a card on a particular board list can
have with the exception of list attached to a particular card"""
from sqlalchemy import Column, String, ForeignKey, UnicodeText, Integer
from models.common import CommonField, Base


class Card(CommonField, Base):
    __tablename__ = "card"
    board_list_id = Column(
        String(50), ForeignKey("board_list.id"), index=True, nullable=False)
    description = Column(UnicodeText())
    position = Column(Integer(), nullable=False, default=0)

    def __init__(self):
        super(Card, self).__init__()
        Card.append_columns(["board_list_id", "description", "position"])
