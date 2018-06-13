#!/usr/bin/env python
"""This module contains the endpoints for interacting with boards in the
system"""
from bottle import Bottle, response, request, json_dumps
from helpers import route_helper
from helpers import jwt_helper
from helpers import exception_helper
from helpers import param_helper

from models.board import Board

app = Bottle(__name__)
route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)


@app.get("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def index():
    return json_dumps(
        Board().list(request.pagination.get("filters", []), request.pagination))


@app.get("/<board_id>")
@app.get("/<board_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(board_id: str):
    return json_dumps(Board().find_by_id(board_id))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    return json_dumps(Board().save(request.data))


@app.put("/<board_id>")
@app.put("/<board_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(board_id: str):
    return json_dumps(Board().update(board_id, request.data))


@app.delete("/<board_id>")
@app.delete("/<board_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(board_id: str):
    return json_dumps(Board().delete(board_id))
