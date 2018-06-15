#!/usr/bin/env python
"""This model defines the users that are attached to a particular board"""
from sqlalchemy import Column, String, ForeignKey
from models.common import CommonField, Base


class BoardUser(CommonField, Base):
    __tablename__ = "board_user"
    board_id = Column(
        String(50), ForeignKey("board.id"), index=True, nullable=False)
    user_id = Column(
        String(50), ForeignKey("users.id"), index=True, nullable=False)

    def __init__(self):
        super(BoardUser, self).__init__()
        BoardUser.append_columns(["board_id", "user_id"])
