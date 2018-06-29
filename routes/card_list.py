#!/usr/bin/env python
"""This module contains the endpoints for interacting with card lists in the
application"""
from copy import deepcopy
from bottle import Bottle, response, request, json_dumps

from helpers import exception_helper
from helpers import jwt_helper
from helpers import param_helper
from helpers import route_helper
from helpers import query_helper
from helpers import log_helper
from helpers import model_helper

from models.card_list import CardList

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
        session, CardList, request.pagination.get("filters", []),
        request.pagination, json_result=True
    )
    return json_dumps([
        model_helper.insert_field_objects(session, row) for row in results
    ])


@app.get("/<card_list_id>")
@app.get("/<card_list_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(card_list_id: str):
    session.rollback()
    result = query_helper.find_by_id(
        session, CardList, card_list_id, json_result=True
    )
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    session.rollback()
    result = query_helper.save(
        session, CardList, request.data, json_result=True)
    log_helper.log_insert(session, CardList, result["id"], result)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.put("/<card_list_id>/<ver>")
@app.put("/<card_list_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(card_list_id: str, ver: str):
    session.rollback()
    data = deepcopy(request.data)
    data.update({"updated_by_id": request.user["id"]})
    old_data = query_helper.find_by_params(
        session, CardList,
        [{"id": {"$eq": card_list_id}}, {"ver": {"$eq": ver}}],
        json_result=True
    )
    result = query_helper.update_by_params(
        session, CardList,
        [{"id": {"$eq": card_list_id}}, {"ver": {"$eq": ver}}],
        data, json_result=True
    )
    log_helper.log_update(session, CardList, result["id"], result, old_data)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.delete("/<card_list_id>/<ver>")
@app.delete("/<card_list_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(card_list_id: str, ver: str):
    session.rollback()
    data = deepcopy(request.data)
    data.update({"deleted_by_id": request.user["id"]})
    old_data = query_helper.find_by_params(
        session, CardList,
        [{"id": {"$eq": card_list_id}}, {"ver": {"$eq": ver}}],
        json_result=True
    )
    result = query_helper.delete_by_params(
        session, CardList,
        [{"id": {"$eq": card_list_id}}, {"ver": {"$eq": ver}}],
        data=data,
        json_result=True
    )
    log_helper.log_update(session, CardList, result["id"], result, old_data)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.get("/<card_list_id>")
@app.get("/<card_list_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def count():
    session.rollback()
    return json_dumps(
        query_helper.count(
            session, CardList, request.paginations.get("filters", [])
        )
    )
