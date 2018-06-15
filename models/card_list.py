#!/usr/bin/env python
"""This defines the list that have been created under a particular card"""
from sqlalchemy import Column, String, ForeignKey, UnicodeText, Boolean
from models.common import CommonField, Base


class CardList(CommonField, Base):
    __tablename__ = "card_list"
    card_id = Column(
        String(50), ForeignKey("card.id"), index=True, nullable=False)
    title = Column(UnicodeText())
    done = Column(Boolean(), default=False)

    def __init__(self):
        super(CardList, self).__init__()
        CardList.append_columns(["card_id", "title", "done"])
