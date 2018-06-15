#!/usr/bin/env python
from bottle import Bottle, response, request, json_dumps
from helpers import route_helper
from helpers import param_helper
from helpers import jwt_helper
from helpers import exception_helper

from models.board_list import BoardList

app = Bottle(__name__)
route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)


@app.get("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def index():
    return json_dumps(
        BoardList().list(
            request.pagination.get('filters', []), request.pagination
        )
    )


@app.get("/<board_list_id>")
@app.get("/<board_list_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(board_list_id: str):
    return json_dumps(BoardList().find_by_id(board_list_id))


@app.put("/<board_list_id>")
@app.put("/<board_list_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(board_list_id: str):
    return json_dumps(BoardList().update_by_id(board_list_id, request.data))


@app.delete("/<board_list_id>")
@app.delete("/<board_list_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(board_list_id: str):
    return json_dumps(BoardList().delete_by_id(board_list_id))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    return json_dumps(BoardList().save(request.data))
