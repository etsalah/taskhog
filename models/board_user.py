#!/usr/bin/env python
"""This model defines the users that are attached to a particular board"""
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from models.common import Base, model_dict


class BoardUser(Base):
    __tablename__ = "board_user"
    id = Column(String(50), primary_key=True)
    board_id = Column(
        String(50), ForeignKey("board.id"), index=True, nullable=False)
    user_id = Column(
        String(50), ForeignKey("users.id"), index=True, nullable=False)
    created_by_id = Column(
        String(50), ForeignKey("users.id"), index=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), index=True, nullable=False,
        default=datetime.now
    )
    deleted_at = Column(DateTime(timezone=True), index=True, nullable=True)
    deleted_by_id = Column(String(50), index=True, nullable=True)
    updated_by_id = Column(String(50), index=True, nullable=True)
    updated_at = Column(DateTime(timezone=True), index=True, nullable=True)
    ver = Column(String(50), nullable=False, index=True)

    COLUMNS = [
        'id', 'created_by_id', 'created_at', 'deleted_at', 'deleted_by_id',
        'updated_by_id', 'updated_at', 'ver', 'board_id', 'user_id'
    ]

    def to_dict(self):
        return model_dict(self)
