#!/usr/bin/env python
"""This module contains the endpoints for interacting with users in the
application"""
from copy import deepcopy
from datetime import datetime

from bottle import Bottle, request, response, json_dumps

from helpers import exception_helper
from helpers import jwt_helper
from helpers import param_helper
from helpers import route_helper
from models.user import User

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
        User().list(
            session, request.pagination.get("filters", []), request.pagination))


@app.get("/<user_id>")
@app.get("/<user_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(user_id):
    return json_dumps(User().find_by_id(session, user_id))


@app.post("/")
def login():
    params = param_helper.get_json(request)
    token = None

    find_args = []
    if 'username' in params:
        find_args.append({'username': {"$eq": params['username']}})

    elif 'email' in params:
        find_args.append({'email': {"$eq": params['email']}})

    if 'password' in params:
        find_args.append({'password': {"$eq": params['password']}})

    result = User().find_by_params(session, find_args)
    if result:
        result = deepcopy(result)
        if 'password' in result:
            del result['password']

        token = jwt_helper.encode_token(result)

    if token:
        result.update({'token': token})
    return json_dumps(result)


@app.post("/create")
@app.post("/create/")
@exception_helper.handle_exception(response)
@param_helper.handle_request_data(request)
def signup():
    data = deepcopy(request.data)
    data.update({
        "created_at": datetime.utcnow()
    })
    result = User().save(session, data)
    return result


@app.put("/<user_id>")
@app.put("/<user_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(user_id):
    data = deepcopy(request.data)
    data.update({
        "updated_by_id": request.user["id"],
        "updated_at": datetime.now()
    })
    return json_dumps(User().update_by_id(session, user_id, data))


@app.delete("/<user_id>")
@app.delete("/<user_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(user_id):
    return json_dumps(User().delete_by_id(session, user_id))


@app.get("/count")
@app.get("/count/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def count():
    return json_dumps(User().count(
        session, request.pagination.get("filters", [])))


@app.get("/decode")
def decode():
    params = param_helper.get_json(request)
    result = jwt_helper.decode_token(params["token"])
    return json_dumps(result)
