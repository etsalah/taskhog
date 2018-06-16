#!/usr/bin/env python
from functools import wraps
import jwt
from sqlalchemy.orm import exc as orm_exc
from sqlalchemy import exc
from json import JSONDecodeError
import custom_exceptions as custom_exc
# from helpers import route_helper


def handle_exception(response_obj):
    """
    This function is used as a decorator to all the endpoints to make sure that
    all exception that might be thrown are handled here
    :param response_obj:  This is the responsible object that will be tag with
        the appropriate status code and message to be returned to the caller of
        endpoint
    :return: callable that is used to wrap the endpoints
    """

    def deco_func(func):

        @wraps(func)
        def wrapping_func(*args, **kwargs):
            # route_helper.patch_response_for_cors(response_obj)
            try:
                result = func(*args, **kwargs)
            except orm_exc.NoResultFound:
                response_obj.status = 404
                result = {
                    'message':
                        'No records was founding matching the request criteria'
                }
            except KeyError as e:
                response_obj.status = 400
                result = {
                    "message": (
                        "You didn't pass the required field '{0}' to "
                        "the endpoint".format(e.args[0])
                    )
                }
            except exc.IntegrityError as e:
                response_obj.status = 400
                result = {"message": e.args[0]}
            except jwt.exceptions.DecodeError:
                response_obj.status = 401
                result = {"message": "Token provided is invalid"}
            except jwt.exceptions.ExpiredSignatureError:
                response_obj.status = 401
                result = {"message": "Token provided has expired"}
            except JSONDecodeError as e:
                response_obj.status = 500
                result = {"message": e.msg}
            except (
                    custom_exc.LoggedOutError, custom_exc.LoginExpiredError,
                    custom_exc.LoginRevokedError, ValueError,
                    custom_exc.TokenAbsentError) as e:
                response_obj.status = 401
                result = {"message": e.message}
            except custom_exc.BaseError as e:
                response_obj.status = 400
                result = {'message': e.message}
            except Exception as e:
                print(" => ", type(e))
                response_obj.status = 500
                result = {"message": str(e)}
            return result

        return wrapping_func
    return deco_func
