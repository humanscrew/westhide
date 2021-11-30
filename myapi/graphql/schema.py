from graphene import Schema
from .types import user, dashboard


class Query(user.Query, dashboard.Query):
    pass


schema = Schema(query=Query)
