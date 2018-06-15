#!/usr/bin/env python
"""This module contains the endpoints for interacting with labels of a board in
the system"""
from bottle import Bottle, response, request, json_dumps
from helpers import route_helper
from helpers import jwt_helper
from helpers import exception_helper
from helpers import param_helper

from models.board_label import BoardLabel

app = Bottle(__name__)
route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)


@app.get("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def index():
    return json_dumps(
        BoardLabel().list(
            request.pagination.get("filters", []), request.pagination))


@app.get("/<board_label_id>")
@app.get("/<board_label_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(board_label_id: str):
    return json_dumps(BoardLabel().find_by_id(board_label_id))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    return json_dumps(BoardLabel().save(request.data))


@app.put("/<board_label_id>")
@app.put("/<board_label_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(board_label_id: str):
    return json_dumps(BoardLabel().update_by_id(board_label_id, request.data))


@app.delete("/<board_label_id>")
@app.delete("/<board_label_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(board_label_id: str):
    return json_dumps(BoardLabel().delete_by_id(board_label_id))
