#!/usr/bin/env python
"""This module contains code that helps generates the necessary queries that
access the database"""
from typing import Dict, List, TypeVar, Any

from dateutil.parser import parse as parse_date
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

SessionType = TypeVar('SessionType', bound=Session)
SUPPORTED_QUERY_OPERATORS = (
    '$ne', '$eq', '$in', '$nin', '$gt', '$gte', '$lt', '$lte'
)


def query(
        session_obj: SessionType, model_cls,
        params: List[Dict], pagination_args: Dict):
    record_set = session_obj.query(model_cls)
    for param in params:
        record_set += _apply_query_param(model_cls, record_set, param)
    record_set = query_sort(
        model_cls, record_set, pagination_args.get("sort", []))
    return query_limit(record_set, pagination_args)


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
                value["$data"], "append") and hasattr(value["$date"], "clear"):
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
