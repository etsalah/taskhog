#!/usr/bin/env python
"""This endpoint contains the endpoints for interacting with card labels in
the system"""
from bottle import Bottle, response, request, json_dumps
from helpers import route_helper
from helpers import jwt_helper
from helpers import exception_helper
from helpers import param_helper

from models.card_label import CardLabel

app = Bottle(__name__)
route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)


@app.get("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def index():
    return json_dumps(
        CardLabel().list(
            request.pagination.get("filters", []), request.pagination))


@app.get("/<card_label_id>")
@app.get("/<card_label_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(card_label_id: str):
    return json_dumps(CardLabel().find_by_id(card_label_id))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    return json_dumps(CardLabel().save(request.data))


@app.put("/<card_label_id>")
@app.put("/<card_label_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(card_label_id: str):
    return json_dumps(CardLabel().update_by_id(card_label_id, request.data))


@app.delete("/<card_label_id>")
@app.delete("/<card_label_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(card_label_id: str):
    return json_dumps(CardLabel().delete_by_id(card_label_id))
