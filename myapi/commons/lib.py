class Lib(object):
    def __init__(self):
        super().__init__()
        pass

    @staticmethod
    def camel2under_score(camel_case: str) -> str:
        if not isinstance(camel_case, str):
            return camel_case
        camel_str_list: list = [
            "_" + item if item.isupper() else item for item in camel_case
        ]
        under_score: str = "".join(camel_str_list).lower()
        return under_score

    @staticmethod
    def del_none_in_list(raw_list):
        if isinstance(raw_list, list):
            deal_list = [item for item in raw_list if item]
            return deal_list
        else:
            return raw_list
