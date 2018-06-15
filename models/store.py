#!/usr/bin/env python
from typing import Dict, List, Tuple, Any
from dateutil.parser import parse as parse_date

SUPPORTED_QUERY_OPERATORS = (
    '$ne', '$eq', '$in', '$nin', '$gt', '$gte', '$lt', '$lte'
)


class Store:

    def __init__(self):
        self._store = []

    @staticmethod
    def to_dict(data: Dict) -> Dict:
        tmp = {}
        for field in data:
            value = data[field]

            if hasattr(value, "day") and hasattr(value, "fromtimestamp"):
                value = str(value)

            tmp[field] = value
        return tmp

    def insert(self, obj):
        self._store.append(obj)
        return Store.to_dict(obj)

    def delete(self, param_list: List[Dict]) -> List[Dict]:
        matched_items, unmatched_items = self._list(param_list)
        self._store = unmatched_items
        return [Store.to_dict(matched_item) for matched_item in matched_items]

    def update(self, param_list: List[Dict], data: Dict) -> List[Dict]:
        tmp = []
        update_items = []
        for item in self._store:
            matched = []
            for param in param_list:
                matched.append(_match_param(param, item))

            not_match_count = matched.count(False)

            if not_match_count == 0:
                item.update(data)
                update_items.append(item)

            tmp.append(item)

        self._store = tmp
        return [Store.to_dict(updated_item) for updated_item in update_items]

    def find_by_id(self, _id) -> Dict:
        result = self.list_objects(
            [{"id": {"$eq": _id}}], {"offset": 0, "limit": 1})
        if result:
            return Store.to_dict(result[0])
        return {}

    def find_by_params(self, param_list: List[Dict]) -> Dict:
        result = self.list_objects(param_list, {"offset": 0, "limit": 1})
        if result:
            return Store.to_dict(result[0])
        return {}

    def list_objects(
            self, param_list: List[Dict] = None,
            pagination: Dict = None) -> List[Dict]:

        if not param_list and not pagination:
            return self._store

        return self._list(param_list, pagination)[0]
    
    def count_objects(self, param_list: List[Dict] = None) -> Dict:
        if not param_list:
            return {"count": len(self._store)}

        return {"count": len(self._list(param_list)[0])}

    def _list(
            self, param_list: List[Dict],
            pagination: Dict = None) -> Tuple[List[Dict], List[Dict]]:
        unmatched_items = []
        matched_items = []

        pagination = {
            'offset': 0,
            'limit': len(self._store)
        } if not pagination else pagination
        offset_count = 0
        limit_count = 0
        for item in self._store:
            matched = []
            for param in param_list:
                matched.append(_match_param(param, item))

            not_matched_count = matched.count(False)

            if not_matched_count == 0 and \
                    offset_count == pagination['offset'] and \
                    limit_count < pagination['limit']:
                matched_items.append(item)
                limit_count += 1
            elif not_matched_count == 0 and offset_count < pagination['offset']:
                offset_count += 1
            else:
                unmatched_items.append(item)

        return (
            [Store.to_dict(matched_item) for matched_item in matched_items],
            [
                Store.to_dict(unmatched_item)
                for unmatched_item in unmatched_items
            ]
        )

    @staticmethod
    def _list_param_parser(param_list: List[Dict] = None):
        if not param_list:
            return param_list

        new_params = []

        for param in param_list:

            for qualifier in SUPPORTED_QUERY_OPERATORS:

                for field in param:

                    if field.get(qualifier) == '$date':
                        if not hasattr(
                                param[field][qualifier],
                                "title") and hasattr(
                                param[field][qualifier], 'append'):

                            new_params[field][qualifier] = [
                                parse_date(date_str)
                                for date_str in param_list[field][qualifier]]

                        elif hasattr(param_list[field][qualifier], "title"):
                            new_params[field][qualifier] = parse_date(
                                param_list[field][qualifier])

        return new_params


def convert_if_date(value: Any):
    if hasattr(value, 'items') and hasattr(value, "fromkeys"):
        return parse_date(value["$date"])
    return value


def _match_param(params: Dict, value: Dict) -> bool:
    for field in params:
        for operator in params[field].keys():
            operator_value = convert_if_date(params[field][operator])
            field_value = value.get(field)
            if operator == "$eq":
                return operator_value == field_value
            elif operator == "$ne":
                return operator_value != field_value
            elif operator == "$lt":
                return field_value < operator_value
            elif operator == "$lte":
                return (
                    field_value < operator_value or
                    field_value == operator_value
                )
            elif operator == "$gt":
                return field_value > operator_value
            elif operator == "$gte":
                return (
                    field_value > operator_value or
                    field_value == operator_value
                )
            elif operator == "$nin":
                return field_value not in operator_value
            elif operator == "$in":
                return field_value in operator_value
