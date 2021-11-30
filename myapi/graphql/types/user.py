from graphene import Node, ObjectType, types
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from myapi.models import User
from .role import RoleType
from flask_jwt_extended import get_jwt_identity


class UserType(SQLAlchemyObjectType):
    roles = types.List(RoleType)

    class Meta:
        model = User
        interfaces = (Node,)
        exclude_fields = (
            "_password",
            "password",
        )
        batching = True


class Query(ObjectType):
    node = Node.Field()
    users = SQLAlchemyConnectionField(UserType)
    user = types.Field(UserType)

    @staticmethod
    def resolve_user(self, info):
        user_id = get_jwt_identity()
        return User.query.get_or_404(user_id)
