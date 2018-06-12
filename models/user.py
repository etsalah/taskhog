#!/usr/bin/env python
from models.common import CommonField


class User(CommonField):
    __tablename__ = "users"
    username = ''
    email = ''
    password = ''
