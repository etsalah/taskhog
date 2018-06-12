#!/usr/bin/env python
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

ENV = os.environ.get("ENV", "DEVELOPMENT")


def env_test(env_name):
    return True if ENV == env_name else False