#!/usr/bin/env python3
"""
This module contains functions for generating and decoding jwt tokens. As well
as code for handling the validity period for tokens in use in the application
"""
from hashlib import md5
from datetime import datetime, timedelta
from functools import wraps
import jwt
from helpers import param_helper
import custom_exceptions


__author__ = "edem.tsalah@gmail.com"

# TODO: change this into a more secure token. Later move this into configure
_SECRET = 'jwt_token_secret'
_LOGIN_VALID_TIME_SPAN = timedelta(minutes=60)
ALGORITHM = 'HS256'


def get_token_checksum(token):
    return md5(bytes(token, "utf-8")).hexdigest()


def encode_token(data):
    """
    This function is responsible for encode the data that is passed to into a
    jwt token
    :param data: data to be used to generate jwt token
    :return: string representing the generated jwt token
    """
    tm = datetime.utcnow() + _LOGIN_VALID_TIME_SPAN
    data.update({"exp": tm})
    token = str(jwt.encode(data, _SECRET, algorithm=ALGORITHM)).lstrip(
        "b'").rstrip("'")
    return token


def decode_token(token):
    """
    This function is used to decode the jwt token into the data that was used to
    generate it
    :param token: token to be decoded
    :return: resulting data from the token decode process
    """
    return jwt.decode(token, _SECRET, algorithms=ALGORITHM)


def handle_token_decode(request_obj):

    def deco_func(func):

        @wraps(func)
        def wrapping_func(*args, **kwargs):
            data = param_helper.get_json(request_obj)
            try:
                setattr(request_obj, 'user', decode_token(data["token"]))
            except KeyError:
                raise custom_exceptions.TokenAbsentError()
            return func(*args, **kwargs)

        return wrapping_func
    return deco_func
