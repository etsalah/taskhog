#!/usr/bin/env python
"""This module contains the endpoints for interacting with users in the
application"""
from copy import deepcopy
from datetime import datetime

from bottle import Bottle, request, response, json_dumps

from helpers import exception_helper
from helpers import jwt_helper
from helpers import log_helper
from helpers import model_helper
from helpers import param_helper
from helpers import password_helper
from helpers import query_helper
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
    session.rollback()
    results = query_helper.list_query(
        session, User, request.pagination.get("filters", []),
        request.pagination, json_result=True
    )
    return json_dumps([
        model_helper.insert_field_objects(session, row) for row in results])


@app.get("/<user_id>")
@app.get("/<user_id>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def find(user_id):
    result = query_helper.find_by_id(session, User, user_id, json_result=True)
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.post("/")
@exception_helper.handle_exception(response)
@param_helper.handle_request_data(request)
def login():
    session.rollback()
    params = request.data
    token = None

    find_args = []
    if 'username' in params:
        find_args.append({'username': {"$eq": str(params['username']).strip()}})

    elif 'email' in params:
        find_args.append({'email': {"$eq": str(params['email']).strip()}})

    if 'password' in params:
        find_args.append({
            'password': {
                "$eq": password_helper.encrypt_password(
                    str(params['password']).strip())
            }
        })

    result = query_helper.find_by_params(
        session, User, find_args, json_result=True)
    if result:
        if 'password' in result:
            del result['password']

        token = jwt_helper.encode_token(result)

    if token:
        result.update({'token': token})

    return json_dumps(model_helper.insert_field_objects(session, result))


@app.post("/create")
@app.post("/create/")
@exception_helper.handle_exception(response)
@param_helper.handle_request_data(request)
@jwt_helper.handle_token_decode(request)
def signup():
    session.rollback()
    data = deepcopy(request.data)
    data.update({
        "created_at": datetime.utcnow(),
        "created_by_id": request.user["id"]
    })
    if 'password' in data:
        data['password'] = password_helper.encrypt_password(
            str(data['password']).strip())

    result = query_helper.save(session, User, data, json_result=True)
    log_helper.log_insert(session, User, result["id"], result)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.put("/<user_id>/<ver>")
@app.put("/<user_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def update(user_id: str, ver: str):
    session.rollback()
    data = deepcopy(request.data)
    data.update({
        "updated_by_id": request.user["id"],
        "updated_at": datetime.now()
    })

    if 'password' in data:
        del data['password']

    old_data = query_helper.find_by_params(
        session, User, [{"id": {"$eq": user_id}}, {"ver": {"$eq": ver}}],
        json_result=True
    )

    result = query_helper.update_by_params(
        session, User, [{"id": {"$eq": user_id}}, {"ver": {"$eq": ver}}],
        data, json_result=True
    )
    log_helper.log_update(session, User, result["id"], result, old_data)
    session.commit()
    return json_dumps(model_helper.insert_field_objects(session, result))


@app.delete("/<user_id>/<ver>")
@app.delete("/<user_id>/<ver>/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def delete(user_id: str, ver: str):
    session.rollback()
    old_data = query_helper.find_by_params(
        session, User, [{"id": {"$eq": user_id}}, {"ver": {"$eq": ver}}],
        json_result=True
    )
    result = query_helper.delete_by_params(
        session, User, [{"id": {"$eq": user_id}}, {"ver": {"$eq": ver}}],
        {'deleted_by_id': request.user['id']},
        json_result=True
    )
    log_helper.log_update(session, User, result["id"], result, old_data)
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
            session, User, request.pagination.get("filters", [])))


@app.get("/decode")
def decode():
    params = param_helper.get_json(request)
    result = jwt_helper.decode_token(params["token"])
    return json_dumps(result)
