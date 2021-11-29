from graphene import Node, List
from graphene_sqlalchemy import SQLAlchemyObjectType
from myapi.models import User
from .role import RoleType


class UserType(SQLAlchemyObjectType):
    role = List(RoleType)

    class Meta:
        model = User
        interfaces = (Node,)
        exclude_fields = (
            "_password",
            "password",
        )
        batching = True
