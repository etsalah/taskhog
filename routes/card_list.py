#!/usr/bin/env python
"""This module contains the endpoints for interacting with card lists in the
application"""
from bottle import Bottle, response, request, json_dumps
from helpers import route_helper
from helpers import jwt_helper
from helpers import exception_helper
from helpers import param_helper

from models.card_list import CardList

app = Bottle(__name__)
route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)


@app.get("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def index():
    return json_dumps(
        CardList().list(
            request.pagination.get("filters", []), request.pagination))


@app.get("/<card_list_id>")
@app.get("/<card_list_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(card_list_id: str):
    return json_dumps(CardList().find_by_id(card_list_id))


@app.post("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def create():
    return json_dumps(CardList().save(request.data))


@app.put("/<card_list_id>")
@app.put("/<card_list_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(card_list_id: str):
    return json_dumps(CardList().update(card_list_id, request.data))


@app.delete("/<card_list_id>")
@app.delete("/<card_list_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(card_list_id: str):
    return json_dumps(CardList().delete(card_list_id))
