#!/usr/bin/env python
from typing import Dict, List, Tuple


class Store:

    def __init__(self):
        self._store = []

    def insert(self, obj):
        self._store.append(obj)

    def delete(self, params: Dict) -> List[Dict]:
        matched_items, unmatched_items = self._list(params)
        self._store = unmatched_items
        return matched_items

    def update(self, params: Dict, data: Dict) -> List[Dict]:
        tmp = []
        update_items = []
        for item in self._store:
            matched = True
            for key in params:
                if params[key] == item.get(key):
                    matched = matched and True
                else:
                    matched = False
                    break

            if matched:
                item.update(data)
                update_items.append(item)

            tmp.append(item)

        self._store = tmp
        return update_items

    def find_by_id(self, _id) -> Dict :
        result = self.list_objects({"id": _id}, {"offset": 0, "limit": 1})
        if result:
            return result[0]
        return {}

    def find_by_params(self, params: Dict) -> Dict:
        result = self.list_objects(params, {"offset": 0, "limit": 1})
        if result:
            return result[0]
        return {}

    def list_objects(
            self, params: Dict = None, pagination: Dict = None) -> List[Dict]:

        if not params and not pagination:
            return self._store

        return self._list(params, pagination)[0]
    
    def count_objects(self, params: Dict = None) -> Dict:
        if not params:
            return {"count": len(self._store)}

        return {"count": len(self._list(params)[0])}

    def _list(
            self, params: Dict,
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
            matched = True
            for key in params:
                if params[key] == item.get(key):
                    matched = matched and True
                else:
                    matched = False
                    break

            if matched and offset_count == pagination['offset'] and \
                    limit_count < pagination['limit']:
                matched_items.append(item)
                limit_count += 1
            elif matched and offset_count < pagination['offset']:
                offset_count += 1
            else:
                unmatched_items.append(item)

        return matched_items, unmatched_items
