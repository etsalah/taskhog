#!/usr/bin/env python
"""This module contains the endpoints for interacting with the users of boards
in the application"""
from bottle import Bottle, response, request, json_dumps
from helpers import route_helper
from helpers import jwt_helper
from helpers import exception_helper
from helpers import param_helper
from helpers import query_helper

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
        query_helper.list_query(
            session, BoardUser,
            request.pagination.get("filters", []),
            request.pagination, json_result=True
        )
    )


@app.get("/<board_user_id>")
@app.get("/<board_user_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(board_user_id: str):
    return json_dumps(
        query_helper.save(
            session, BoardUser, board_user_id, json_result=True))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    result = query_helper.save(
        session, BoardUser, request.data, json_result=True)
    session.commit()
    return json_dumps(result)


@app.put("/<board_user_id>/<ver>")
@app.put("/<board_user_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(board_user_id: str, ver: str):
    result = query_helper.update_by_params(
        session, BoardUser, [{"id": board_user_id}, {"ver": ver}],
        request.data, json_result=True)
    session.commit()
    return json_dumps(result)


@app.delete("/<board_user_id>/<ver>")
@app.delete("/<board_user_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(board_user_id: str, ver: str):
    result = query_helper.delete_by_params(
        session, BoardUser, [{"id": board_user_id}, {"ver": ver}],
        json_result=True
    )
    session.commit()
    return json_dumps(result)


@app.get("/count")
@app.get("/count/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def count():
    return json_dumps(
        query_helper.count(
            session, BoardUser, request.pagination.get("filters", [])
        )
    )
