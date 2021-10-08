from myapi.utils import Lib
from myapi.commons import paginate as rawPaginate


class HandleQuery:

    def __init__(self, model):
        self.model = model
        self.query = model.query
        self.columns = model.__table__.columns.keys()

    def sort(self, sorter):
        for item in sorter:
            field = item.get("field")
            field = Lib.camel2UnderScore(field)
            type = item.get("type")

            if field in self.columns and type:
                self.query = self.query.order_by(getattr(getattr(self.model, field), type)())

        return self

    def filterIn(self, filter):
        for item in filter:
            field = item.get("field")
            field = Lib.camel2UnderScore(field)
            values = item.get("values")

            if field in self.columns and values:
                self.query = self.query.filter(getattr(self.model, field).in_(values))

        return self

    def paginate(self, schema, isDelUrl=True):
        paginateResult = rawPaginate(self.query, schema)
        if isDelUrl:
            del paginateResult["prev"]
            del paginateResult["next"]
        return paginateResult
