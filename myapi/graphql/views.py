from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from myapi.commons import CipherHook

from flask_graphql import GraphQLView
from .schema import schema

blueprint = Blueprint("graphql", __name__, url_prefix="/westhide")

blueprint.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, batch=True, graphiql=True),
)


@blueprint.before_request
@jwt_required()
def before_request():
    if request.method == "POST" and not request.is_json:
        return {"message": "Missing JSON in request"}, 405
    return CipherHook.decrypt_request()


@blueprint.after_request
def after_request(response):
    return CipherHook.encrypt_response(response)
