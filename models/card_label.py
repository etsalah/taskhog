#!/usr/bin/env python
"""This model defines contains the details of the board labels that are
attached to a specific card"""
from datetime import datetime
from sqlalchemy import String, ForeignKey, Column, DateTime
from models.common import Base, model_dict


class CardLabel(Base):
    __tablename__ = "card_label"
    id = Column(String(50), primary_key=True)
    board_label_id = Column(
        String(50), ForeignKey("board_label.id"), index=True, nullable=False)
    card_id = Column(
        String(50), ForeignKey("card.id"), index=True, nullable=False)
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
        'updated_by_id', 'updated_at', 'ver', 'board_label_id', 'card_id'
    ]

    def to_dict(self):
        return model_dict(self)
