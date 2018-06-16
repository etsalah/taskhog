#!/usr/bin/env python
"""This module contains a definition of the basic fields that all the models in
the system and the crud operation that can be performed on these models"""
from datetime import datetime
from typing import List, AnyStr, Dict

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from helpers import id_helper
from models.store import Store

test_store = {}

Base = declarative_base()


def model_dict(obj):
    tmp = {}
    for column in obj.COLUMNS:
        value = getattr(obj, column)
        if hasattr(value, "day") and hasattr(value, "fromordinal"):
            value = str(value)
        tmp[column] = value

    return tmp


class CommonField:
    __tablename__ = ""
    id = Column(String(50), primary_key=True)
    created_by_id = Column(
        "created_by_id", String(50), index=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), index=True, nullable=False,
        default=datetime.now
    )
    deleted_at = Column(DateTime(timezone=True), index=True, nullable=True)
    deleted_by_id = Column(String(50), index=True, nullable=True)
    updated_by_id = Column(String(50), index=True, nullable=True)
    updated_at = Column(DateTime(timezone=True), index=True, nullable=True)
    ver = Column(String(50), nullable=False, index=True)

    COLUMNS = [
        'id', 'created_by_id', 'created_at', 'deleted_at', 'deleted_by_id',
        'updated_by_id', 'updated_at', 'ver'
    ]

    def dict(self):
        tmp = {}
        for column in CommonField.COLUMNS:
            tmp[column] = getattr(self, column)

        return tmp

    @staticmethod
    def sanitize_data(data):
        tmp = {}
        if 'token' in data:
            del data['token']

        for column in CommonField.COLUMNS:
            if column in data:
                tmp[column] = data[column]
        return tmp

    @staticmethod
    def append_columns(columns: List[AnyStr]):
        CommonField.COLUMNS.extend(columns)


def get_db(store_name: AnyStr):
    global test_store
    if store_name not in test_store:
        test_store[store_name] = Store()

    return test_store[store_name]


def save(store_name: AnyStr, data: Dict):
    if 'id' not in data:
        data['id'] = id_helper.generate_id()
    return get_db(store_name).insert(data)


def update_by_id(store_name: AnyStr, _id: AnyStr, data: Dict):
    result = get_db(store_name).update([{'id': {'$eq': _id}}], data)
    return result[0] if result else {}


def update_by_params(store_name: AnyStr, params: List[Dict], data: Dict):
    result = get_db(store_name).update(params, data)
    return result[0] if result else {}


def find_by_id(store_name: AnyStr, _id: AnyStr):
    return get_db(store_name).find_by_id(_id)


def find_by_params(store_name: AnyStr, params: List[Dict]):
    return get_db(store_name).find_by_params(params)


def list_objects(
        store_name: AnyStr, params: List[Dict],
        pagination_args: Dict=None) -> List[Dict]:
    return get_db(store_name).list_objects(params, pagination_args)


def delete_by_id(store_name: AnyStr, _id: AnyStr):
    result = get_db(store_name).delete([{"id": {'$eq': _id}}])
    return result[0] if result else {}


def delete_by_params(store_name: AnyStr, params: List[Dict]):
    result = get_db(store_name).delete(params)
    return result[0] if result else {}


def count(store_name: AnyStr, params: List[Dict]=None):
    return get_db(store_name).count_objects(params)
