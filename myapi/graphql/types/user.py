from graphene import Node, ObjectType, types, Connection
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

from myapi.models import User
from .role import RoleConnectionField, RoleConnection
from flask_jwt_extended import get_jwt_identity


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {"username": [...]}


class UserConnectionField(FilterableConnectionField):
    filters = {
        User: UserFilter(),
    }


class UserType(SQLAlchemyObjectType):
    role = RoleConnectionField(RoleConnection)

    class Meta:
        model = User
        interfaces = (Node,)
        exclude_fields = (
            "_password",
            "password",
        )
        batching = True
        # connection_field_factory = UserConnectionField.factory


class UserConnection(Connection):
    class Meta:
        node = UserType


class Query(ObjectType):
    node = Node.Field()
    user = types.Field(UserType)
    users = UserConnectionField(UserConnection)

    @staticmethod
    def resolve_user(parent, info):
        user_id = get_jwt_identity()
        return User.query.get_or_404(user_id)
