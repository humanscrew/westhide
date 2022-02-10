from graphene import Node, Connection
from graphene_sqlalchemy import SQLAlchemyObjectType
from myapi.struct.models import Role
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet


class RoleFilter(FilterSet):
    class Meta:
        model = Role
        fields = {"name": [...]}


class RoleConnectionField(FilterableConnectionField):
    filters = {
        Role: RoleFilter(),
    }


class RoleType(SQLAlchemyObjectType):
    class Meta:
        model = Role
        interfaces = (Node,)
        batching = True


class RoleConnection(Connection):
    class Meta:
        node = RoleType
