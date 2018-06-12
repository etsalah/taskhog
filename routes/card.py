#!/usr/bin/env python
from bottle import Bottle, response
from helpers import route_helper

app = Bottle(__name__)
route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)


@app.get("/")
def index():
    return "card"
