#!/usr/bin/env python
"""This defines the list that have been created under a particular card"""
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, UnicodeText, Boolean
from sqlalchemy import DateTime
from models.common import Base, model_dict


class CardList(Base):
    __tablename__ = "card_list"
    id = Column(String(50), primary_key=True)
    card_id = Column(
        String(50), ForeignKey("card.id"), index=True, nullable=False)
    title = Column(UnicodeText())
    done = Column(Boolean(), default=False)
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
        'updated_by_id', 'updated_at', 'ver', 'card_id', 'title', 'done'
    ]

    def to_dict(self):
        return model_dict(self)
