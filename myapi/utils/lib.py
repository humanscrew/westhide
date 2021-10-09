
class LibABC(object):

    def __init__(self):
        super().__init__()
        pass

    def camel2UnderScore(self, camelCase: str) -> str:
        if not isinstance(camelCase, str):
            return camelCase
        camelstrList: list = ["_" + item if item.isupper() else item for item in camelCase]
        underScore: str = "".join(camelstrList).lower()
        return underScore

    def delNoneInList(self, rawlist):
        if isinstance(rawlist, list):
            dealList = [item for item in rawlist if item]
            return dealList
        else:
            return rawlist


Lib = LibABC()
