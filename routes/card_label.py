#!/usr/bin/env python
"""This endpoint contains the endpoints for interacting with card labels in
the system"""
from bottle import Bottle, response, request, json_dumps
from helpers import route_helper
from helpers import jwt_helper
from helpers import exception_helper
from helpers import param_helper
from helpers import query_helper

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
    return json_dumps(
        query_helper.list_query(
            session, CardLabel,
            request.pagination.get("filters", []),
            request.pagination, json_result=True
        )
    )


@app.get("/<card_label_id>")
@app.get("/<card_label_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(card_label_id: str):
    return json_dumps(
        query_helper.find_by_id(
            session, CardLabel, card_label_id,
            json_result=True
        )
    )


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    result = query_helper.save(
        session, CardLabel, request.data, json_result=True)
    session.commit()
    return json_dumps(result)


@app.put("/<card_label_id>/<ver>")
@app.put("/<card_label_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(card_label_id: str, ver: str):
    result = query_helper.update_by_params(
        session, CardLabel,
        [{"id": card_label_id}, {"ver": ver}], request.data,
        json_result=True
    )
    session.commit()
    return json_dumps(result)


@app.delete("/<card_label_id>/<ver>")
@app.delete("/<card_label_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(card_label_id: str, ver: str):
    result = query_helper.delete_by_params(
        session, CardLabel, [{"id": card_label_id}, {"ver": ver}],
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
            session, CardLabel, request.pagination.get("filters", [])
        )
    )
