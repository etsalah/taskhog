#!/usr/bin/env python
import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine

from models import common

load_dotenv(find_dotenv(), override=True)

ENV = os.environ.get("ENV", "DEVELOPMENT")
DB_ENGINE = None
ENGINE_DICT = {}
DB_ECHO = True if str(
    os.environ.get("DB_ECHO", "False")).upper() == "TRUE" else False


def env_test(env_name):
    return True if ENV == env_name else False


def get_connection_str():
    con_str = os.environ.get("{0}_DB".format(ENV), None)
    if not con_str:
        raise Exception(
            "You need to set the environmental variable for "
            "the {0} environment".format(ENV)
        )
    return con_str


def create_engine_():
    global DB_ENGINE
    if DB_ENGINE not in ENGINE_DICT:
        ENGINE_DICT[DB_ENGINE] = create_engine(
            get_connection_str(),
            echo=DB_ECHO
        )

    return ENGINE_DICT[DB_ENGINE]


def create_db(engine):
    common.Base.metadata.create_all(engine)
