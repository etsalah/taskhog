#!/usr/bin/env python
"""This module contains the endpoint for interacting with cards in the
application"""
from copy import deepcopy

from bottle import Bottle, response, request, json_dumps

from helpers import exception_helper
from helpers import jwt_helper
from helpers import log_helper
from helpers import model_helper
from helpers import param_helper
from helpers import query_helper
from helpers import route_helper
from models.card import Card

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
        session, Card,
        request.pagination.get("filters", []),
        request.pagination, json_result=True
    )
    return json_dumps([
        model_helper.insert_field_objects(session, row) for row in results
    ])


@app.get("/<card_id>")
@app.get("/<card_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(card_id: str):
    session.rollback()
    result = query_helper.find_by_id(session, Card, card_id, json_result=True)
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    session.rollback()
    data = deepcopy(request.data)
    data.update({"created_by_id": request.user["id"]})
    result = query_helper.save(session, Card, data, json_result=True)
    log_helper.log_insert(session, Card, result["id"], result)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.put("/<card_id>/<ver>")
@app.put("/<card_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(card_id: str, ver: str):
    session.rollback()
    data = deepcopy(request.data)
    data.update({"updated_by_id": request.user["id"]})
    old_data = query_helper.find_by_params(
        session, Card,
        [{"id": {"$eq": card_id}}, {"ver": {"$eq": ver}}], json_result=True
    )
    result = query_helper.update_by_params(
        session, Card, [{"id": {"$eq": card_id}}, {"ver": {"$eq": ver}}],
        data
    )
    log_helper.log_update(session, Card, result["id"], result, old_data)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.delete("/<card_id>/<ver>")
@app.delete("/<card_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(card_id: str, ver: str):
    session.rollback()
    data = deepcopy(request.data)
    data.update({"deleted_by_id": request.user["id"]})
    old_data = query_helper.find_by_params(
        session, Card, [{"id": {"$eq": card_id}}, {"ver": {"$eq": ver}}],
        json_result=True
    )
    result = query_helper.delete_by_params(
        session, Card, [{"id": {"$eq": card_id}}, {"ver": {"$eq": ver}}],
        data=data, json_result=True
    )
    log_helper.log_update(session, Card, result["id"], result, old_data)
    session.commit()
    return json_dumps(result)


@app.delete("/count")
@app.delete("/count/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def count():
    session.rollback()
    return json_dumps(
        query_helper.count(session, Card, request.pagination.get("filters", []))
    )
