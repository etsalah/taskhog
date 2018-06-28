#!/usr/bin/env python
import hashlib


def encrypt_password(password: str) -> str:
    encrypt_pwd = hashlib.sha384(bytes(str(password).strip(), 'utf-8'))
    return encrypt_pwd.hexdigest()
