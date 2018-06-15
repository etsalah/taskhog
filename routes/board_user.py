#!/usr/bin/env python
"""This module contains the endpoints for interacting with the users of boards
in the application"""
from bottle import Bottle, response, request, json_dumps
from helpers import route_helper
from helpers import jwt_helper
from helpers import exception_helper
from helpers import param_helper

from models.board_user import BoardUser

app = Bottle(__name__)
route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)
session = None


@app.get("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def index():
    return json_dumps(
        BoardUser().list(
            session, request.pagination.get("filters", []), request.pagination))


@app.get("/<board_user_id>")
@app.get("/<board_user_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(board_user_id: str):
    return json_dumps(BoardUser().find_by_id(session, board_user_id))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    return json_dumps(BoardUser().save(session, request.data))


@app.put("/<board_user_id>")
@app.put("/<board_user_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(board_user_id: str):
    return json_dumps(
        BoardUser().update_by_id(session, board_user_id, request.data))


@app.delete("/<board_user_id>")
@app.delete("/<board_user_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(board_user_id: str):
    return json_dumps(BoardUser().delete_by_id(session, board_user_id))
