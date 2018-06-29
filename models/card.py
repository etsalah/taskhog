#!/usr/bin/env python
"""This model defines the fields that a card on a particular board list can
have with the exception of list attached to a particular card"""
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, UnicodeText
from sqlalchemy import Integer, DateTime
from models.common import Base, model_dict


class Card(Base):
    __tablename__ = "card"
    id = Column(String(50), primary_key=True)
    board_list_id = Column(
        String(50), ForeignKey("board_list.id"), index=True, nullable=False)
    description = Column(UnicodeText())
    position = Column(Integer(), nullable=False, default=0)
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
        'updated_by_id', 'updated_at', 'ver', 'board_list_id', 'description',
        'position'
    ]

    def to_dict(self):
        return model_dict(self)


class CardLog(Base):
    __tablename__ = "card_log"
    id = Column(String(50), primary_key=True)
    entity_id = Column(
        String(50), ForeignKey("card.id"), nullable=False, index=True)
    previous_state = Column(UnicodeText())
    current_state = Column(UnicodeText())
    created_by_id = Column(
        String(50), ForeignKey("users.id"), index=True, nullable=False),
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
