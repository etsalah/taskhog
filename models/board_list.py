#!/usr/bin/env python
"""This model defines"""
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, UnicodeText, DateTime
from models.common import Base, model_dict


class BoardList(Base):
    __tablename__ = "board_list"
    id = Column(String(50), primary_key=True)
    board_id = Column(
        String(50), ForeignKey("board.id"), index=True, nullable=False)
    title = Column(UnicodeText())
    created_by_id = Column(
        String(50), ForeignKey("users.id"), index=True,
        nullable=False
    )
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
        'updated_by_id', 'updated_at', 'ver', 'board_id', 'title'
    ]

    def to_dict(self):
        return model_dict(self)


class BoardListLog(Base):
    __tablename__ = "board_list_log"
    id = Column(String(50), primary_key=True)
    entity_id = Column(
        String(50), ForeignKey("board_list.id"), nullable=False, index=True)
    previous_state = Column(UnicodeText())
    current_state = Column(UnicodeText())
    created_by_id = Column(
        String(50), ForeignKey("users.id"), index=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), index=True, nullable=False,
        default=datetime.now
    )
    COLUMNS = (
        'id', 'entity_id', 'previous_state', 'current_state', 'created_by_id',
        'created_at'
    )

    def to_dict(self):
        return model_dict(self)
