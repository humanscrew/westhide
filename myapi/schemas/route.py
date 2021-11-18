from myapi.extensions import ma, db
from myapi.models import Route, RouteClosureTable, RouteMeta, RouteTree


class RouteMetaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RouteMeta
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)


class RouteSchema(ma.SQLAlchemyAutoSchema):

    route_meta = ma.Nested(RouteMetaSchema, data_key="meta")

    class Meta:
        model = Route
        sqla_session = db.session
        load_instance = True
        exclude = ("alias",)


class RouteClosureTableSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RouteClosureTable
        sqla_session = db.session
        load_instance = True
        include_fk = True
        exclude = ("id",)


class RouteTreeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RouteTree
        sqla_session = db.session
        load_instance = True
