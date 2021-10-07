
class LibABC(object):

    def camel2UnderScore(self, camelCase: str) -> str:
        camelstrList: list = ["_" + item if item.isupper() else item for item in camelCase]
        underScore: str = "".join(camelstrList).lower()
        return underScore


Lib = LibABC()
