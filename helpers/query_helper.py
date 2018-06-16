#!/usr/bin/env python
"""This module contains code that helps generates the necessary queries that
access the database"""
from datetime import datetime
from typing import Dict, List, TypeVar, Any

from dateutil.parser import parse as parse_date
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from helpers import id_helper

SessionType = TypeVar('SessionType', bound=Session)
SUPPORTED_QUERY_OPERATORS = (
    '$ne', '$eq', '$in', '$nin', '$gt', '$gte', '$lt', '$lte'
)


def sanitize_data(model_cls, data):
    tmp = {}
    if 'token' in data:
        del data['token']

    for column in model_cls.COLUMNS:
        if column in data:
            tmp[column] = data[column]
    return tmp


def query(
        session_obj: SessionType, model_cls,
        params: List[Dict], pagination_args: Dict, json_result=False):
    record_set = session_obj.query(model_cls)
    for param in params:
        record_set = _apply_query_param(model_cls, record_set, param)
    record_set = query_sort(
        model_cls, record_set, pagination_args.get("sort", []))
    result = query_limit(record_set, pagination_args)
    if not json_result:
        return result

    return [row.to_dict() for row in result]


def query_limit(record_set, pagination_args: Dict):
    if pagination_args.get("offset", 0) > 0:
        record_set = record_set.offset(pagination_args["offset"])

    if pagination_args.get("limit", 0) > 0:
        record_set = record_set.limit(pagination_args["limit"])

    return record_set


def query_sort(model_cls, record_set, sort_params: List[List]):
    for sort_param in sort_params:
        for (field, ordering) in sort_param:
            if str(ordering).upper() == "ASC":
                order_func = asc
            elif str(ordering).upper() == "DESC":
                order_func = desc
            else:
                raise NotImplementedError(
                    "{0} isn't a valid ordering functions".format(ordering))
            record_set.order_by(order_func(getattr(model_cls, field)))
    return record_set


def convert_if_date(value: Any):
    if hasattr(value, 'items') and hasattr(value, "fromkeys"):
        if hasattr(
                value["$date"], "append") and hasattr(value["$date"], "clear"):
            return [parse_date(date_val) for date_val in value["$date"]]
        return parse_date(value["$date"])
    return value


def _apply_query_param(model_cls, record_set, params: Dict) -> bool:
    for field in params:
        for operator in params[field].keys():
            operator_value = convert_if_date(params[field][operator])
            if operator == "$eq":

                if operator_value is None:
                    return record_set.filter(
                        getattr(model_cls, field).is_(None))

                return record_set.filter(
                    getattr(model_cls, field) == operator_value)

            elif operator == "$ne":
                return record_set.filter(
                    getattr(model_cls, field) != operator_value)
            elif operator == "$lt":
                return record_set.filter(
                    getattr(model_cls, field) < operator_value)
            elif operator == "$lte":
                return record_set.filter(
                    getattr(model_cls, field) < operator_value |
                    getattr(model_cls, field) == operator_value
                )
            elif operator == "$gt":
                return record_set.filter(
                    getattr(model_cls, field) > operator_value)
            elif operator == "$gte":
                return record_set.filter(
                    getattr(model_cls, field) > operator_value |
                    getattr(model_cls, field) == operator_value
                )
            elif operator == "$nin":
                return record_set.filter(
                    getattr(model_cls, field).notin_(operator_value))
            elif operator == "$in":
                return record_set.filter(
                    getattr(model_cls, field).in_(operator_value))


def save(session_obj, model_cls, data, json_result=False):
    clean_data = sanitize_data(model_cls, data)
    obj = model_cls()
    for field in model_cls.COLUMNS:
        if field in clean_data:
            setattr(obj, field, clean_data[field])

    if "id" not in clean_data:
        setattr(obj, "id", id_helper.generate_id())

    setattr(obj, "ver", id_helper.generate_id())
    session_obj.add(obj)
    if not json_result:
        return obj
    return obj.to_dict()


def update_by_id(session_obj, model_cls, _id, data, json_result=False):
    return update_by_params(
        session_obj, model_cls, [{"id": {"$eq": _id}}], data, json_result)


def update_by_params(
        session_obj, model_cls, params: List[Dict], data, json_result=False):
    clean_data = sanitize_data(model_cls, data)
    if "ver" not in clean_data:
        clean_data["ver"] = id_helper.generate_id()

    found_obj = find_by_params(session_obj, model_cls, params)
    for field in model_cls.COLUMNS:
        if field in clean_data:
            setattr(found_obj, field, clean_data[field])

    session_obj.add(found_obj)
    if not json_result:
        return found_obj
    return found_obj.to_dict()


def delete_by_id(session_obj, model_cls, _id, json_result=False):
    return delete_by_params(
        session_obj, model_cls, [{"id": {"$eq": _id}}], json_result)


def delete_by_params(
        session_obj, model_cls, params: List[Dict], json_result=False):
    return update_by_params(
        session_obj, model_cls, params,
        {"deleted": True, "deleted_at": datetime.utcnow()}, json_result)


def find_by_id(session_obj, model_cls, _id, json_result=False):
    return find_by_params(
        session_obj, model_cls, [{"id": {"$eq": _id}}], json_result)


def find_by_params(
        session_obj, model_cls, params: List[Dict], json_result=False):
    result = list_query(
        session_obj, model_cls, params, {"offset": 0, "limit": 1}, json_result)
    for row in result:
        return row


def list_query(
        session_obj, model_cls, params: List[Dict]=None,
        pagination_args: Dict=None, json_result=False):
    return query(session_obj, model_cls, params, pagination_args, json_result)


def count(session_obj, model_cls, params: List[Dict]=None):
    # TODO: change this to use CommonFields.list
    result = list_query(session_obj, model_cls, params, {})

    count_ = 0
    if result:
        count_ = result.count()

    return {"count": count_}
