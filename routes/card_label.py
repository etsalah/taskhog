#!/usr/bin/env python
"""This endpoint contains the endpoints for interacting with card labels in
the system"""
from copy import deepcopy
from bottle import Bottle, response, request, json_dumps
from helpers import route_helper
from helpers import jwt_helper
from helpers import exception_helper
from helpers import param_helper
from helpers import query_helper
from helpers import model_helper

from models.card_label import CardLabel

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
        session, CardLabel,
        request.pagination.get("filters", []),
        request.pagination, json_result=True
    )
    return json_dumps([
        model_helper.insert_field_objects(session, row) for row in results
    ])


@app.get("/<card_label_id>")
@app.get("/<card_label_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(card_label_id: str):
    session.rollback()
    result = query_helper.find_by_id(
        session, CardLabel, card_label_id,
        json_result=True
    )
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    session.rollback()
    data = deepcopy(request.data)
    data.update({"created_by_id": request.user["id"]})
    result = query_helper.save(session, CardLabel, data, json_result=True)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.put("/<card_label_id>/<ver>")
@app.put("/<card_label_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(card_label_id: str, ver: str):
    session.rollback()
    data = deepcopy(request.data)
    data.update({"updated_by_id": request.user["id"]})
    result = query_helper.update_by_params(
        session, CardLabel,
        [{"id": {"$eq": card_label_id}}, {"ver": {"$eq": ver}}], data,
        json_result=True
    )
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.delete("/<card_label_id>/<ver>")
@app.delete("/<card_label_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(card_label_id: str, ver: str):
    session.rollback()
    data = deepcopy(request.data)
    data.update({"deleted_by_id": request.user["id"]})
    result = query_helper.delete_by_params(
        session, CardLabel,
        [{"id": {"$eq": card_label_id}}, {"ver": {"$eq": ver}}],
        data=data, json_result=True
    )
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
            session, CardLabel, request.pagination.get("filters", [])
        )
    )
