#!/usr/bin/env python
from functools import wraps


def get_pagination_details(request_obj):
    """
    This function is used to get data sent with request that are used during
    pagination of data returned by endpoints that return a list of items.
    This function also provide default values for values that have been sent
    during the request

    :param request_obj: request object that pagination data will be attached to
    :return: dict representing pagination information
    """

    params = get_json(request_obj)

    return {
        'id': params.get('id', ''),
        'limit': int(params.get('limit', 20)),
        'order': params.get('order', 'asc'),
        'offset': int(params.get('offset', 0)),
        'before_id': params.get('before_id', None),
        'after_id': params.get('after_id', None)
    }


def get_json(request_obj):
    """
    This function is responsible for getting the json data that was sent with
    with a request or return an empty dict if no data is sent

    :param request_obj: request object that data should be attached to
    :return: dict
    """
    result = {}
    if not hasattr(request_obj, 'json') or not request_obj.json:
        if hasattr(request_obj, 'params'):
            result = request_obj.params
        return result

    return request_obj.json


def handle_request_data(request_obj):

    def deco(func):

        @wraps(func)
        def wrapping_func(*args, **kwargs):
            setattr(request_obj, 'data', get_json(request_obj))
            setattr(
                request_obj, 'pagination', get_pagination_details(request_obj))
            return func(*args, **kwargs)

        return wrapping_func

    return deco
