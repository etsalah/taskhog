#!/usr/bin/env python
"""This model represents the labels that have been created for a particular
board"""
from sqlalchemy import Column, String, ForeignKey
from models.common import CommonField


class BoardLabel(CommonField):
    __tablename__ = "board_label"
    name = Column(String(200), nullable=False, index=True, unique=True)
    colour = Column(String(50), nullable=False, index=True)
    board_id = Column(
        String(50), ForeignKey("board.id"), nullable=False, index=True)

    def __init__(self):
        super(BoardLabel, self).__init__()
        BoardLabel.append_columns(["name", "colour", "board_id"])
