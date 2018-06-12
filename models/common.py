#!/usr/bin/env python
from models.store import Store
from typing import List, AnyStr, Dict
from helpers import env_test
from helpers import id_helper

test_store = {}


class CommonField:
    __tablename__ = ""
    id = ''
    created_by_id = ''
    created_at = ''
    deleted_at = ''
    deleted_by_id = ''
    updated_by_id = ''
    updated_at = ''
    ver = ''
    is_test = env_test("TEST")

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
        if 'token' in data:
            del data
        return data

    @staticmethod
    def append_columns(columns: List[AnyStr]):
        CommonField.COLUMNS.extend(columns)

    def save(self, data):
        clean_data = CommonField.sanitize_data(data)
        if self.is_test:
            return save(self.__tablename__, clean_data)
        pass

    def update(self, _id, data):
        clean_data = CommonField.sanitize_data(data)
        if self.is_test:
            return update(self.__tablename__, _id, clean_data)

    def find_by_id(self, _id):
        if self.is_test:
            return find_by_id(self.__tablename__, _id)

    def find_by_params(self, params: Dict):
        clean_data = CommonField.sanitize_data(params)
        if self.is_test:
            return find_by_params(self.__tablename__, clean_data)

    def list(self, params: Dict=None, pagination_args: Dict=None) -> List[Dict]:
        clean_data = CommonField.sanitize_data(params)
        if self.is_test:
            return list_objects(self.__tablename__, clean_data, pagination_args)

    def delete(self, _id):
        if self.is_test:
            return delete(self.__tablename__, _id)

    def count(self, params: Dict=None):
        clean_data = CommonField.sanitize_data(params)
        if self.is_test:
            return count(self.__tablename__, clean_data)


def get_db(store_name: AnyStr):
    global test_store
    if store_name not in test_store:
        test_store[store_name] = Store()

    return test_store[store_name]


def save(store_name: AnyStr, data: Dict):
    if 'id' not in data:
        data['id'] = id_helper.generate_id()
    get_db(store_name).insert(data)
    return data


def update(store_name: AnyStr, _id: AnyStr, data: Dict):
    result = get_db(store_name).update({'id': _id}, data)
    return result[0] if result else {}


def find_by_id(store_name: AnyStr, _id: AnyStr):
    return get_db(store_name).find_by_id(_id)


def find_by_params(store_name: AnyStr, params: Dict):
    return get_db(store_name).find_by_params(params)


def list_objects(
        store_name: AnyStr, params: Dict,
        pagination_args: Dict=None) -> List[Dict]:
    return get_db(store_name).list_objects(params, pagination_args)


def delete(store_name: AnyStr, _id: AnyStr):
    result = get_db(store_name).delete({"id": _id})
    return result[0] if result else {}


def count(store_name: AnyStr, params: Dict=None):
    return get_db(store_name).count_objects(params)
