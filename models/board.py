#!/usr/bin/env python
"""This contains the model that represents the boards in the system"""
from datetime import datetime
from sqlalchemy import Column, String, UnicodeText, DateTime, ForeignKey
from models.common import Base, model_dict


class Board(Base):
    __tablename__ = "board"
    id = Column(String(50), primary_key=True)
    name = Column(String(500), nullable=False, unique=True, index=True)
    description = Column(UnicodeText())
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
        'updated_by_id', 'updated_at', 'ver', 'name', 'description'
    ]

    def to_dict(self):
        return model_dict(self)
