#!/usr/bin/env python
from bottle import Bottle, request, response, json_dumps
from helpers import param_helper
from helpers import jwt_helper
from helpers import route_helper
from helpers import exception_helper
from models.user import User


app = Bottle(__name__)
route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)


@app.get("/")
@exception_helper.handle_exception(response)
@jwt_helper.handle_token_decode(request)
@param_helper.handle_request_data(request)
def index():
    print("here")
    print("data =>", request.data, "pagination => ", request.pagination)
    return json_dumps(User().list(request.data, request.pagination))


@app.get("/<user_id>")
@app.get("/<user_id>/")
def find(user_id):
    return json_dumps(User().find_by_id(user_id))


@app.post("/")
def login():
    params = param_helper.get_json(request)
    token = None
    find_args = {}
    if 'username' in params:
        find_args['username'] = params['username']

    elif 'email' in params:
        find_args['email'] = params['email']

    if 'password' in params:
        find_args['password'] = params['password']

    result = User().find_by_params(find_args)
    if result:
        if 'password' in result:
            del result['password']

        token = jwt_helper.encode_token(result)

    if token:
        result.update({'token': token})
    return json_dumps(result)


@app.post("/create")
def signup():
    params = param_helper.get_json(request)
    result = User().save(params)
    return result


@app.put("/<user_id>")
@app.put("/<user_id>/")
def update(user_id):
    params = param_helper.get_json(request)
    return json_dumps(User().update(user_id, params))


@app.delete("/<user_id>")
@app.delete("/<user_id>/")
def delete(user_id):
    return json_dumps(User().delete(user_id))


@app.get("/count")
@app.get("/count/")
def count():
    params = param_helper.get_json(request)
    return json_dumps(User().count(params))


@app.get("/decode")
def decode():
    params = param_helper.get_json(request)
    result = jwt_helper.decode_token(params["token"])
    return json_dumps(result)
