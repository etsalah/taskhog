#!/usr/bin/env python
from datetime import datetime

from bottle import Bottle, response
from sqlalchemy.orm import sessionmaker

import config
from helpers import query_helper
from helpers import route_helper
from helpers import password_helper
from models.user import User
from routes import board
from routes import board_label
from routes import board_list
from routes import board_user
from routes import card
from routes import card_label
from routes import card_list
from routes import user

engine = config.create_engine_()
SessionMaker = sessionmaker(bind=engine)

session = SessionMaker()

app = Bottle(__name__)

routes = [
    ('/board', board.app, board),
    ('/board_label', board_label.app, board_label),
    ('/board_list', board_list.app, board_list),
    ('/board_user', board_user.app, board_user),
    ('/card', card.app, card),
    ('/card_label', card_label.app, card_label),
    ('/card_list', card_list.app, card_list),
    ('/user', user.app, user)
]

for route in routes:
    app.mount(route[0], route[1])
    route[2].session = session


route_helper.enable_cor(app, response)
route_helper.handle_options_call(app)


@app.get("/")
def index():
    return "Hello world"


def setup_admin_account(_id):

    if not query_helper.find_by_id(session, User, _id):
        query_helper.save(
            session,
            User,
            {
                "id": _id,
                "email": "super@gmail.com",
                "username": "super",
                "password": password_helper.encrypt_password(
                    str("password").strip()),
                "created_by_id": _id,
                "created_at": datetime.utcnow()
            }
        )
        session.commit()


if __name__ == '__main__':
    DEBUG = config.env_test('DEVELOPMENT')
    config.create_db(engine)
    setup_admin_account("0")
    app.run(debug=DEBUG, port=9091)
