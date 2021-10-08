
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


Lib = LibABC()
