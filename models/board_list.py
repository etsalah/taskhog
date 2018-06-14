#!/usr/bin/env python
"""This model defines"""
from sqlalchemy import Column, String, ForeignKey, UnicodeText
from models.common import CommonField


class BoardList(CommonField):
    __tablename__ = "board_list"
    board_id = Column(
        String(50), ForeignKey("board.id"), index=True, nullable=False)
    user_id = Column(
        String(50), ForeignKey("users.id"), index=True, nullable=False)
    title = Column(UnicodeText())

    def __init__(self):
        super(BoardList, self).__init__()
        BoardList.append_columns(["board_id", "user_id", "title"])
