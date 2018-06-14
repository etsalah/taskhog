#!/usr/bin/env python
"""This model defines contains the details of the board labels that are
attached to a specific card"""
from sqlalchemy import String, ForeignKey, Column
from models.common import CommonField


class CardLabel(CommonField):
    __tablename__ = "card_label"
    board_label_id = Column(
        String(50), ForeignKey("board_label.id"), index=True, nullable=False)
    card_id = Column(
        String(50), ForeignKey("card.id"), index=True, nullable=False)

    def __init__(self):
        super(CardLabel, self).__init__()
        CardLabel.append_columns(["board_label_id", "card_id"])
