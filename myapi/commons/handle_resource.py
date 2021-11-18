from flask import jsonify
from sqlalchemy.sql.expression import or_
from .lib import Lib
from .pagination import paginate as common_paginate


class HandleQuery:
    def __init__(self, model, schema=None, request=None):
        self.model = model
        self.query = model.query
        self.columns = model.__table__.columns.keys()
        self.schema = schema
        self.request = request.args or request.json

    def sort(self, sorter=None):
        sorter = sorter or self.request.get("sorter")
        if not sorter:
            return self
        for item in sorter:
            field = item.get("field")
            field = Lib.camel2under_score(field)
            sort_type = item.get("type")

            if field in self.columns and type:
                self.query = self.query.order_by(
                    getattr(getattr(self.model, field), sort_type)()
                )

        return self

    def filter_in(self, filter_in=None):
        filter_in = filter_in or self.request.get("filterIn")
        if not filter_in:
            return self
        for item in filter_in:
            field = item.get("field")
            field = Lib.camel2under_score(field)
            values = item.get("values")

            if field in self.columns and values:
                self.query = self.query.filter(getattr(self.model, field).in_(values))

        return self

    def filter_like(self, filter_like=None):
        filter_like = filter_like or self.request.get("filterLike")
        if not filter_like:
            return self
        for item in filter_like:
            field = item.get("field")
            field = Lib.camel2under_score(field)
            values = item.get("values")
            values = Lib.del_none_in_list(values)

            if field in self.columns and values:
                self.query = self.query.filter(
                    or_(
                        *[
                            getattr(self.model, field).like("%" + val + "%")
                            for val in values
                        ]
                    ),
                )

        return self

    def between(self, between=None):
        between = between or self.request.get("between")
        if not between:
            return self
        for item in between:
            field = item.get("field")
            field = Lib.camel2under_score(field)
            left = item.get("left")
            right = item.get("right")
            if field in self.columns and left and right:
                self.query = self.query.filter(
                    getattr(self.model, field).between(left, right)
                )

        return self

    def with_entities(self, with_entities=None):
        with_entities = with_entities or self.request.get("withEntities")
        if not with_entities:
            return self
        for field in with_entities:
            field = Lib.camel2under_score(field)

            if field in self.columns:
                self.query = self.query.with_entities(getattr(self.model, field))

        return self

    def distinct(self, distinct=None):
        distinct = distinct or self.request.get("distinct")
        if not distinct:
            return self
        self.query = self.query.distinct()

        return self

    def limit(self, limit):
        limit = limit or self.request.get("limit")
        if not limit:
            return self
        self.query = self.query.limit(limit)

        return self

    def offset(self, offset):
        offset = offset or self.request.get("offset")
        if not offset:
            return self
        self.query = self.query.offset(offset)

        return self

    def deal(
        self,
        sorter=None,
        filter_in=None,
        filter_like=None,
        between=None,
        with_entities=None,
        distinct=None,
        limit=None,
        offset=None,
    ):
        self.sort(sorter)
        self.filter_in(filter_in)
        self.filter_like(filter_like)
        self.between(between)
        self.with_entities(with_entities)
        self.distinct(distinct)
        self.limit(limit)
        self.offset(offset)
        return self

    def paginate(self, schema=None, link=None):
        if not schema:
            schema = self.schema
        paginate = common_paginate(self.query, schema, link)
        return jsonify(paginate)


class HandleObjects:
    def __init__(self, collection, schema=None, request=None):
        self.collection = collection
        self.objects = collection.objects
        self.documents = list(self.collection._fields.keys())
        self.schema = schema
        self.request = request.args or request.json

    def sort(self, sorter=None):
        sorter = sorter or self.request.get("sorter")
        if not sorter:
            return self
        for item in sorter:
            field = item.get("field")
            sort_type = item.get("type")

            if field in self.documents and sort_type:
                order = "+" + field if sort_type == "asc" else "-" + field
                self.objects = self.objects.order_by(order)

        return self

    def filter_in(self, filter_in=None):
        filter_in = filter_in or self.request.get("filterIn")
        if not filter_in:
            return self
        for item in filter_in:
            field = item.get("field")
            values = item.get("values")

            if field in self.documents and values:
                field = field + "__in"
                self.objects = self.objects(**{field: values})

        return self

    def filter_like(self, filter_like=None):
        filter_like = filter_like or self.request.get("filterLike")
        if not filter_like:
            return self
        for item in filter_like:
            field = item.get("field")
            values = item.get("values")
            values = Lib.del_none_in_list(values)

            if field in self.documents and values:
                field = field + "__contains"
                for value in values:
                    self.objects = self.objects(**{field: value})

        return self

    def with_entities(self, with_entities=None):
        with_entities = with_entities or self.request.get("withEntities")
        if not with_entities:
            return self
        for field in with_entities:
            if field in self.documents:
                self.objects = self.objects.only(field)

        return self

    def distinct(self, distinct=None, field=None):
        distinct = distinct or self.request.get("distinct")
        fields = field or self.request.get("withEntities")
        if not distinct or fields:
            return self
        self.objects = self.objects.distinct(fields[0])

        return self

    def limit(self, limit):
        limit = limit or self.request.get("limit")
        if not limit:
            return self
        self.objects = self.objects.limit(limit)

        return self

    def offset(self, offset):
        offset = offset or self.request.get("offset")
        if not offset:
            return self
        self.objects = self.objects.skip(offset)

        return self

    def deal(
        self,
        sorter=None,
        filter_in=None,
        filter_like=None,
        with_entities=None,
        distinct=None,
        limit=None,
        offset=None,
    ):
        self.sort(sorter)
        self.filter_in(filter_in)
        self.filter_like(filter_like)
        self.with_entities(with_entities)
        self.distinct(distinct)
        self.limit(limit)
        self.offset(offset)
        return self

    def paginate(self, schema=None, page=None, per_page=None):
        if not schema:
            schema = self.schema
        page = page or self.request.get("page")
        per_page = per_page or self.request.get("per_page")
        total = self.objects.count()
        if page and per_page:
            self.offset((page - 1) * per_page)
            self.limit(per_page)
        return {"pages": page, "result": schema.dump(self.objects), "total": total}
