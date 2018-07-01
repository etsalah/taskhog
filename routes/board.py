#!/usr/bin/env python
"""This module contains the endpoints for interacting with boards in the
system"""
from copy import deepcopy
from datetime import datetime

from bottle import Bottle, response, request, json_dumps

from helpers import exception_helper
from helpers import jwt_helper
from helpers import log_helper
from helpers import model_helper
from helpers import param_helper
from helpers import query_helper
from helpers import route_helper
from models.board import Board, BoardLog

app = Bottle(__name__)
route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)
session = None


@app.get("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def index():
    session.rollback()
    results = query_helper.list_query(
        session, Board, request.pagination.get("filters", []),
        request.pagination, json_result=True
    )
    return json_dumps([
        model_helper.insert_field_objects(session, row) for row in results
    ])


@app.get("/<board_id>")
@app.get("/<board_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(board_id: str):
    session.rollback()
    result = query_helper.find_by_id(session, Board, board_id)
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    session.rollback()
    data = deepcopy(request.data)
    data.update({
        "created_by_id": request.user["id"], "created_at": datetime.now()})
    result = query_helper.save(session, Board, data, json_result=True)
    log_helper.log_insert(session, Board, request.user["id"], result)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.put("/<board_id>/<ver>")
@app.put("/<board_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(board_id: str, ver: str):
    session.rollback()
    data = deepcopy(request.data)
    data.update({"updated_by_id": request.user["id"]})
    old_data = query_helper.find_by_params(
        session, Board, [{"id": {"$eq": board_id}}, {"ver": {"$eq": ver}}],
        json_result=True
    )
    result = query_helper.update_by_params(
        session, Board, [{"id": {"$eq": board_id}}, {"ver": {"$eq": ver}}],
        data, json_result=True
    )
    log_helper.log_update(session, Board, request.user["id"], result, old_data)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.delete("/<board_id>/<ver>")
@app.delete("/<board_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(board_id: str, ver: str):
    session.rollback()
    old_data = query_helper.find_by_params(
        session, Board, [{"id": {"$eq": board_id}}, {"ver": {"$eq": ver}}],
        json_result=True
    )
    result = query_helper.delete_by_params(
        session, Board, [{"id": {"$eq": board_id}}, {"ver": {"$eq": ver}}],
        data={"deleted_by_id": request.user["id"]}, json_result=True
    )
    log_helper.log_update(session, Board, request.user["id"], result, old_data)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.get("/count")
@app.get("/count/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def count():
    session.rollback()
    return json_dumps(
        query_helper.count(
            session, Board,
            request.pagination.get("filters", [])
        )
    )


@app.get("<board_id>/logs")
@app.get("<board_id>/logs/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def log(board_id: str):
    session.rollback()
    return json_dumps(
        query_helper.list_query(
            session, BoardLog, [{"entity_id": {"$eq": board_id}}],
            json_result=True
        )
    )
