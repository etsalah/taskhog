#!/usr/bin/env python
"""This contains the model that represents the boards in the system"""
from sqlalchemy import Column, String, UnicodeText
from models.common import CommonField


class Board(CommonField):
    __tablename__ = "board"
    name = Column(String(500), nullable=False, unique=True, index=True)
    description = Column(UnicodeText())

    def __init__(self):
        super(Board, self).__init__()
        Board.append_columns(["name", "description"])
