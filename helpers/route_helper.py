#!/usr/bin/env python
"""
This module contains functions that are applied to particular routes as a whole
"""
__author__ = "edem.tsalah@gmail.com"


def enable_cor(app_obj, response_obj):
    """
    This function is used to add cors support to application instance that is
    pass to it

    :param app_obj: application instance that should have cors enabled for it
    :param response_obj: response object that cors related headers will be set
        on
    :return: None
    """
    @app_obj.hook("after_request")
    def wrapper():
        patch_response_for_cors(response_obj)


def handle_options_call(app_obj):
    """
    This function is used to support `OPTIONS` request to application instance
    passed to it

    :param app_obj: application instance that `OPTIONS` request support should
        be enabled for
    :return: None
    """

    @app_obj.route("/", method=['OPTIONS'])
    @app_obj.route("/<path:path>", method=['OPTIONS'])
    def options_handler(path=None):
        return


def patch_response_for_cors(response_obj):
    methods = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    headers = 'Origin, Accept, Content-Type, X-Request-With, X-CSRF-Token'
    response_obj.headers['Access-Control-Allow-Origin'] = "*"
    response_obj.headers['Access-Control-Allow-Methods'] = methods
    response_obj.headers['Access-Control-Allow-Headers'] = headers
