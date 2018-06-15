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
    ('/board', board.app, board.session),
    ('/board_label', board_label.app, board_label.session),
    ('/board_list', board_list.app, board_list.session),
    ('/board_user', board_user.app, board_user.session),
    ('/card', card.app, card.session),
    ('/card_label', card_label.app, card_label.session),
    ('/card_list', card_list.app, card_list.session),
    ('/user', user.app, user.session)
]

for route in routes:
    app.mount(route[0], route[1])
    route[2].session = session


route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)


@app.get("/")
def index():
    return "Hello world"


if __name__ == '__main__':
    DEBUG = config.env_test('DEVELOPMENT')
    config.create_db(engine)
    app.run(debug=DEBUG, port=9091)
