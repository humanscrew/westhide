from flask import jsonify
from myapi.utils import Lib
from myapi.commons import paginate as raw_paginate
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
                    or_(*[getattr(self.model, field).like("%" + val + "%") for val in values]), )

        return self

    def between(self, between=None):
        between = between or self.request.get('between')
        if not between:
            return self
        for item in between:
            field = item.get("field")
            field = Lib.camel2UnderScore(field)
            left = item.get("left")
            right = item.get("right")
            if field in self.columns and left and right:
                self.query = self.query.filter(getattr(self.model, field).between(left, right))

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

        return self

    def offset(self, offset):
        offset = offset or self.request.get('offset')
        if not offset:
            return self
        self.query = self.query.offset(offset)

        return self

    def deal(self, sorter=None, filterIn=None, filterLike=None, between=None, withEntities=None, distinct=None,
             limit=None, offset=None):
        self.sort(sorter)
        self.filterIn(filterIn)
        self.filterLike(filterLike)
        self.between(between)
        self.withEntities(withEntities)
        self.distinct(distinct)
        self.limit(limit)
        self.offset(offset)
        return self

    def paginate(self, schema=None, link=None):
        if not schema:
            schema = self.schema
        paginateResult = raw_paginate(self.query, schema, link)
        return jsonify(paginateResult)


class HandleObjects:

    def __init__(self, collection, schema=None, request={}):
        self.collection = collection
        self.objects = collection.objects
        self.documents = list(self.collection._fields.keys())
        self.schema = schema
        self.request = request.args or request.json

    def sort(self, sorter=None):
        sorter = sorter or self.request.get('sorter')
        if not sorter:
            return self
        for item in sorter:
            field = item.get("field")
            type = item.get("type")

            if field in self.documents and type:
                order = "+" + field if type == "asc" else "-" + field
                self.objects = self.objects.order_by(order)

        return self

    def filterIn(self, filter=None):
        filter = filter or self.request.get('filterIn')
        if not filter:
            return self
        for item in filter:
            field = item.get("field")
            values = item.get("values")

            if field in self.documents and values:
                field = field + "__in"
                self.objects = self.objects(**{field: values})

        return self

    def filterLike(self, filter=None):
        filter = filter or self.request.get('filterLike')
        if not filter:
            return self
        for item in filter:
            field = item.get("field")
            values = item.get("values")
            values = Lib.delNoneInList(values)

            if field in self.documents and values:
                field = field + "__contains"
                for value in values:
                    self.objects = self.objects(**{field: value})

        return self

    def withEntities(self, withEntities=None):
        withEntities = withEntities or self.request.get('withEntities')
        if not withEntities:
            return self
        for field in withEntities:
            if field in self.documents:
                self.objects = self.objects.only(field)

        return self

    def distinct(self, distinct=None, field=None):
        distinct = distinct or self.request.get('distinct')
        fields = field or self.request.get('withEntities')
        if not distinct or fields:
            return self
        self.objects = self.objects.distinct(fields[0])

        return self

    def limit(self, limit):
        limit = limit or self.request.get('limit')
        if not limit:
            return self
        self.objects = self.objects.limit(limit)

        return self

    def offset(self, offset):
        offset = offset or self.request.get('offset')
        if not offset:
            return self
        self.objects = self.objects.skip(offset)

        return self

    def deal(self, sorter=None, filterIn=None, filterLike=None, withEntities=None, distinct=None, limit=None,
             offset=None):
        self.sort(sorter)
        self.filterIn(filterIn)
        self.filterLike(filterLike)
        self.withEntities(withEntities)
        self.distinct(distinct)
        self.limit(limit)
        self.offset(offset)
        return self

    def paginate(self, schema=None, page=None, per_page=None):
        if not schema:
            schema = self.schema
        page = page or self.request.get('page')
        per_page = per_page or self.request.get('per_page')
        total = self.objects.count()
        if page and per_page:
            self.offset((page - 1) * per_page)
            self.limit(per_page)
        return {"pages": page, "result": schema.dump(self.objects), "total": total}
