from myapi.utils import Lib
from myapi.commons import paginate as rawPaginate
from sqlalchemy.sql.expression import or_


class HandleQuery:

    def __init__(self, model, schema=None, request={}):
        self.model = model
        self.query = model.query
        self.columns = model.__table__.columns.keys()
        self.schema = schema
        self.request = request.args or request.json

    def sort(self, sorter=None):
        sorter = sorter or self.request.get('sorter')
        if not sorter:
            return self
        for item in sorter:
            field = item.get("field")
            field = Lib.camel2UnderScore(field)
            type = item.get("type")

            if field in self.columns and type:
                self.query = self.query.order_by(getattr(getattr(self.model, field), type)())

        return self

    def filterIn(self, filter=None):
        filter = filter or self.request.get('filterIn')
        if not filter:
            return self
        for item in filter:
            field = item.get("field")
            field = Lib.camel2UnderScore(field)
            values = item.get("values")

            if field in self.columns and values:
                self.query = self.query.filter(getattr(self.model, field).in_(values))

        return self

    def filterLike(self, filter=None):
        filter = filter or self.request.get('filterLike')
        if not filter:
            return self
        for item in filter:
            field = item.get("field")
            field = Lib.camel2UnderScore(field)
            values = item.get("values")
            values = Lib.delNoneInList(values)

            if field in self.columns and values:
                self.query = self.query.filter(
                    or_(*[getattr(self.model, field).like("%"+val+"%") for val in values]),)

        return self

    def withEntities(self, withEntities=None):
        withEntities = withEntities or self.request.get('withEntities')
        if not withEntities:
            return self
        for field in withEntities:
            field = Lib.camel2UnderScore(field)

            if field in self.columns:
                self.query = self.query.with_entities(getattr(self.model, field))

        return self

    def distinct(self, distinct=None):
        distinct = distinct or self.request.get('distinct')
        if not distinct:
            return self
        self.query = self.query.distinct()

        return self

    def limit(self, limit):
        limit = limit or self.request.get('limit')
        if not limit:
            return self
        self.query = self.query.limit(limit)

    def offset(self, offset):
        offset = offset or self.request.get('limit')
        if not offset:
            return self
        self.query = self.query.offset(offset)

    def deal(self, sorter=None, filterIn=None, filterLike=None, withEntities=None, distinct=None, limit=None, offset=None):
        self.sort(sorter)
        self.filterIn(filterIn)
        self.filterLike(filterLike)
        self.withEntities(withEntities)
        self.distinct(distinct)
        self.limit(limit)
        self.offset(offset)
        return self

    def paginate(self, schema=None, isDelUrl=True):
        if not schema:
            schema = self.schema
        paginateResult = rawPaginate(self.query, schema)
        if isDelUrl:
            del paginateResult["prev"]
            del paginateResult["next"]
        return paginateResult
