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
    """This function is used to remove any key value pairs in the dictionary
    used to create or update entities in the system

    Arg(s)
    ------
    model_cls -> The model whose column fields are being looked up in the
        dictionary
    data (dict) -> The dictionary that we whose value pairs that are not in the
        models columns are being removed

    Return(s)
    ---------
    tmp (dict) -> The new dictionary with the new key value pairs that match
        the models column
    """
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
    """This function is responsible for returning a filter list of model
    instances from the database.

    Arg(s):
    -------
    session_obj (SessionType) -> The object used to interact with the data model
    model_cls -> Model class that represents the database table to get data from
    params (List[Dict]) -> The list of filter condictions that will be used to
        filter the data that is returned
    pagination_args (Dict) -> The paginations arguments that indicates how many
        entities to be returned from the database and how many records to be
        skipped
    json_result (bool) -> indicates whether the data returned is a list of model
        instances or a list of dictionaries representing each model instance
        that is returned which

    Return(s):
    ----------
        returns a list of instance of class passed in the model_cls param or
        list of dictionaries representing
    """
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
    """This function applies the pagination arguments to the record set that is
    passed to it

    Arg(s)
    ------
    record_set -> the record set object that needs the pagination arguments
        applied to it
    pagination_args (Dict) -> the pagination arguments that need to be applied
        to the record set

    Return(s)
    ---------
    record_set -> a new record set with the pagination arguments applied to it
    """
    if pagination_args.get("offset", 0) > 0:
        record_set = record_set.offset(pagination_args["offset"])

    if pagination_args.get("limit", 0) > 0:
        record_set = record_set.limit(pagination_args["limit"])

    return record_set


def query_sort(model_cls, record_set, sort_params: List[List]):
    """This function is responsible for applying a sort to a particular record
    set

    Arg(s)
    ------
    model_cls -> class representing the model whose record set we to sort
    record_set -> instance of the record set that the sort must be applied to
    sort_params (List[List]) -> the list of sort that need to be applied to the
        record set

    Return(s)
    ---------
    record_set -> returns a new record set with the sort params applied to it
    """
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
    """This function converts the value passed to it to a date or list of dates
    if it is annotated as containing a date. This is necessary because dates are
    not natively supported in json

    Args(s):
    --------
    value -> the value to be converted to a native date value if it's a date

    Return(s):
    ----------
    returns the same value field if it is not annotated as contains a date or
    it returns a native date or list of native date values
    """
    if hasattr(value, 'items') and hasattr(value, "fromkeys"):
        if hasattr(
                value["$date"], "append") and hasattr(value["$date"], "clear"):
            return [parse_date(date_val) for date_val in value["$date"]]
        return parse_date(value["$date"])
    return value


def _apply_query_param(model_cls, record_set, params: Dict) -> bool:
    """This function is responsible for applying a filter parameter to a
    record set

    Arg(s)
    ------
    model_cls -> class representing the model that the filter parameter must be
        applied
    record_set -> record set instance that the filter parameter must be applied
    params (Dict) -> Dictionary that represents the filtering paramater that
        must be applied

    Return(s)
    ---------
    returns a new record set instance with the filtering parameter applied to it
    """
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


def save(session_obj: SessionType, model_cls, data, json_result=False):
    """This function is responsible for storing a new instance of the model into
    the database

    Arg(s):
    -------
    session_obj -> object used to interact with the database
    model_cls -> class that represents the model that need to be saved in to
        the dataabase
    data (Dict) -> Dictionary that contains the fields (columns) and values that
        need to be set on the model before saving the model instance into the
        database
    json_result (bool) ->  indicates whether a json representation of the model
        instance that was just saved should be returned or the raw instance

    Return(s):
    ----------
    returns either a dictionary or instance of the model_cls depending on the
    value of json_result
    """
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

    """This function is responsible for updating a particular instance of a
    model when the id of that instance is known

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class that represents the model whose instance needs to be
        updated
    _id -> id of the instance of the model that needs to be updated
    data (dict) -> Dictionary that contains the fields that need to be updated
        and the values that they need to be set to
    json_result (bool) -> indicates whether the new state of the model's
        instance should be returned raw or converted to a dictionary

    Return(s)
    ---------
    returns a raw instance of the model or a dictionary representing the model
    """
    return update_by_params(
        session_obj, model_cls, [{"id": {"$eq": _id}}], data, json_result)


def update_by_params(
        session_obj: SessionType, model_cls, params: List[Dict], data,
        json_result=False):
    """This function is updates the instance of the model represented by the
    class in model_cls and identified by the arguments in the params parameter

    Arg(s)
    ------
    session_obj: the object used to interact with the database
    model_cls: class representing the model whose instance needs to be updated
    params (List[Dict]) -> parameters that will be used to identify the model
        instance that needs to be updated
    data (Dict) -> the fields that need to be updated with the values in the
        parameter
    json_result (bool) -> indicates whether the resulting instances of the model
        needs to be converted to a dictionary or the raw instance needs to be
        returned

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
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


def delete_by_id(session_obj: SessionType, model_cls, _id, json_result=False):
    """This function is used to update an instance of the class indicated by
    id in _id

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class representing the model that needs to be updated
    _id -> id of the instance of the class that needs to be deleted
    json_result (bool) -> indicates whether the deleted instance should be
        returned raw or converted to a dictionary

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    return delete_by_params(
        session_obj, model_cls, [{"id": {"$eq": _id}}], json_result)


def delete_by_params(
        session_obj: SessionType, model_cls, params: List[Dict],
        json_result=False):
    """This function is used to update an instance of the class indicated by
    parameters in the params argument

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class representing the model that needs to be updated
    params (List[Dict]) -> parameters that can be used to identify the instance
        of the model to be deleted
    json_result (bool) -> indicates whether the deleted instance should be
        returned raw or converted to a dictionary

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    return update_by_params(
        session_obj, model_cls, params,
        {"deleted": True, "deleted_at": datetime.utcnow()}, json_result)


def find_by_id(session_obj: SessionType, model_cls, _id, json_result=False):
    """This function is responsible for finding the instance of the model that
    is identified by value in the _id argument

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class representing instance of the model to be found
    _id -> id of the model to be found
    json_result -> indicates whether the found object used b returned as a
        dictionary or a raw instance

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    return find_by_params(
        session_obj, model_cls, [{"id": {"$eq": _id}}], json_result)


def find_by_params(
        session_obj: SessionType, model_cls, params: List[Dict],
        json_result=False):
    """This function is responsible for finding the instance of the model that
    is identified by filter parameters in params

    Arg(s)
    ------
    session_obj -> object used to interact with the database
    model_cls -> class representing instance of the model to be found
    params -> list of parameters to find a instance of the model class by
    json_result -> indicates whether the found object used b returned as a
        dictionary or a raw instance

    Return(s)
    ---------
    returns raw instance or dictionary representing the raw instance based on
    json_result's value
    """
    result = list_query(
        session_obj, model_cls, params, {"offset": 0, "limit": 1}, json_result)
    for row in result:
        return row


def list_query(
        session_obj: SessionType, model_cls, params: List[Dict]=None,
        pagination_args: Dict=None, json_result=False):
    """This function is responsible for returning a list of model instances

    Arg(s):
    -------
    session_obj -> object used to interact with the database
    model_cls -> class that represents the model instances to be returned
    params (List[Dict]) -> List of parameters to used to filter the instances of
        model class instances to be returned
    pagination_args (Dict) -> parameter that indicate how many matched instances
        of the model classes to return and how many matched instances of the
        model classes to skip

    Return(s):
    ---------
    List of model class instances either a raw class instances or as a list of
    dictionaries
    """
    return query(session_obj, model_cls, params, pagination_args, json_result)


def count(session_obj: SessionType, model_cls, params: List[Dict]=None):
    """This function is responsible for returning the number of instances of a 
    model match a list of filter parameters

    Arg(s):
    ------
    session_obj -> object used to interact with the database
    model_cls -> model classes whose instances we want to count
    params (List[Dict]) -> parameter to used to filter the instances to be
        counted

    Return(s):
    ----------
    dictionary representing the count of the instances that matched params
    """
    result = list_query(session_obj, model_cls, params, {})

    count_ = 0
    if result:
        count_ = result.count()

    return {"count": count_}
