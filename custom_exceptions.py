#!/usr/bin/env python3


class BaseError(Exception):
    def __init__(self, message):
        self.message = message


class LoggedOutError(BaseError):
    def __init__(self):
        super(LoggedOutError, self).__init__("User is currently not logged In")
        # self.message = "User is currently not logged In"


class LoginExpiredError(BaseError):
    def __init__(self):
        super(LoginExpiredError, self).__init__("User log in has expired")


class LoginRevokedError(BaseError):
    def __init__(self):
        super(LoginRevokedError, self).__init__(
            "User's logged access has been revoked")


class TokenAbsentError(BaseError):
    def __init__(self):
        super(TokenAbsentError, self).__init__(
            "You need to pass in token for user making this request")
