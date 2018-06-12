#!/usr/bin/env python
from uuid import uuid4


def generate_id():
    return str(uuid4()).replace("-", "")
