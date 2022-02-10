from flask import json
from datetime import datetime, date


class Lib:
    @staticmethod
    def camel2under_score(camel_case: str | list) -> str | list:
        if isinstance(camel_case, str):
            camel_str_list = [
                "_" + item if item.isupper() else item for item in camel_case
            ]
            under_score = "".join(camel_str_list).lower()
            return under_score
        if isinstance(camel_case, list):
            return [Lib.camel2under_score(item) for item in camel_case]
        return camel_case

    @staticmethod
    def del_none_in_list(raw_list):
        if isinstance(raw_list, list):
            deal_list = [item for item in raw_list if item]
            return deal_list
        else:
            return raw_list

    @staticmethod
    def camel_case(self, field_name, field_obj):
        string = field_obj.data_key or field_name
        parts = iter(string.split("_"))
        field_obj.data_key = next(parts) + "".join(item.title() for item in parts)


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        from decimal import Decimal

        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        return super().default(obj)
