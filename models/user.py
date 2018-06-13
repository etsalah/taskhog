#!/usr/bin/env python
"""This model defines the details of the users that would be tracked in the
application"""
from models.common import CommonField


class User(CommonField):
    __tablename__ = "users"
    username = ''
    email = ''
    password = ''
