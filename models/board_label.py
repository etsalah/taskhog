#!/usr/bin/env python
"""This model represents the labels that have been created for a particular
board"""
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from models.common import Base, model_dict


class BoardLabel(Base):
    __tablename__ = "board_label"
    id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False, index=True, unique=True)
    colour = Column(String(50), nullable=False, index=True)
    board_id = Column(
        String(50), ForeignKey("board.id"), nullable=False, index=True)
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
        'updated_by_id', 'updated_at', 'ver', 'name', 'colour', 'board_id'
    ]

    def to_dict(self):
        return model_dict(self)
