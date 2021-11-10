
class Lib(object):

    def __init__(self):
        super().__init__()
        pass

    @staticmethod
    def camel2UnderScore(camelCase: str) -> str:
        if not isinstance(camelCase, str):
            return camelCase
        camelstrList: list = ["_" + item if item.isupper() else item for item in camelCase]
        underScore: str = "".join(camelstrList).lower()
        return underScore

    @staticmethod
    def delNoneInList(rawlist):
        if isinstance(rawlist, list):
            dealList = [item for item in rawlist if item]
            return dealList
        else:
            return rawlist
