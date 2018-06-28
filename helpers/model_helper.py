#!/usr/bin/env python
from models.user import User
from models.card import Card
from models.board import Board
from helpers import query_helper

FIELD_MODEL_MAPPING = {
    'created_by_id': {'cls': User, 'label': 'created_by'},
    'updated_by_id': {'cls': User, 'label': 'updated_by'},
    'deleted_by_id': {'cls': User, 'label': 'deleted_by'},
    'user_id': {'cls': User, 'label': 'user'},
    'card_id': {'cls': Card, 'label': 'card'},
    'board_id': {'cls': Board, 'label': 'board'}
}


def insert_field_objects(session_obj, obj_dict: dict):
    mapped_columns = FIELD_MODEL_MAPPING.keys()

    for column in mapped_columns:
        if column in obj_dict:
            if obj_dict[column]:
                label = FIELD_MODEL_MAPPING[column]["label"]
                cls = FIELD_MODEL_MAPPING[column]["cls"]
                obj_dict[label] = query_helper.find_by_id(
                    session_obj, cls, obj_dict[column], json_result=True)

    return obj_dict
