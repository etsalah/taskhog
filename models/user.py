#!/usr/bin/env python
"""This model defines the details of the users that would be tracked in the
application"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from models.common import Base, model_dict


class User(Base):
    __tablename__ = "users"
    id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), index=True, nullable=False)
    password = Column(String(200), index=True, nullable=False)
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

    COLUMNS = (
        'username', 'email', 'password', 'id', 'created_by_id', 'created_at',
        'deleted_at', 'deleted_by_id', 'updated_by_id', 'updated_at', 'ver',
    )

    def to_dict(self):
        return model_dict(self)
