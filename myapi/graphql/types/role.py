from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType
from myapi.models import Role


class RoleType(SQLAlchemyObjectType):
    class Meta:
        model = Role
        interfaces = (Node,)
        batching = True
