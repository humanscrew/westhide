from flask import Blueprint
from flask_graphql import GraphQLView
from .schema import schema

blueprint = Blueprint("graphql", __name__, url_prefix="/westhide/graphql")

blueprint.add_url_rule(
    "/", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)
