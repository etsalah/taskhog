#!/usr/bin/env python
"""This model defines the details of the users that would be tracked in the
application"""
from sqlalchemy import Column, String
from models.common import CommonField


class User(CommonField):
    __tablename__ = "users"
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), index=True, nullable=False)
    password = Column(String(100), index=True, nullable=False)

    def __init__(self):
        super(User, self).__init__()
        User.append_columns(["username", "email", "password"])
