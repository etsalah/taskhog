#!/usr/bin/env python
from bottle import Bottle, response
from sqlalchemy.orm import sessionmaker
from helpers import route_helper
from routes import board
from routes import board_label
from routes import board_list
from routes import board_user
from routes import card
from routes import card_label
from routes import card_list
from routes import user
import config


engine = config.create_engine_()
SessionMaker = sessionmaker(bind=engine)

session = SessionMaker()

app = Bottle(__name__)

routes = [
    ('/board', board.app), ('/board_label', board_label.app),
    ('/board_list', board_list.app), ('/board_user', board_user.app),
    ('/card', card.app), ('/card_label', card_label.app),
    ('/card_list', card_list.app), ('/user', user.app)
]

for route in routes:
    app.mount(route[0], route[1])


route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)


@app.get("/")
def index():
    return "Hello world"


if __name__ == '__main__':
    DEBUG = config.env_test('DEVELOPMENT')
    config.create_db(engine)
    app.run(debug=DEBUG, port=9091)
