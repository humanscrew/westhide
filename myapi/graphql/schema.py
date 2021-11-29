from graphene import ObjectType, Schema, relay, Field
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .types import UserType
from myapi.models import User


class Query(ObjectType):
    node = relay.Node.Field()
    users = SQLAlchemyConnectionField(UserType)
    user = Field(UserType)

    @staticmethod
    def resolve_user(self, info):
        return User.query.first()


schema = Schema(query=Query)
