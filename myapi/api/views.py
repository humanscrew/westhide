from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from flask_jwt_extended import jwt_required

from marshmallow import ValidationError

from myapi.extensions import apispec
from myapi.api.resources import (
    RootPage,
    UserResource, UserList,
    PermitCodeResource,
    RouteResource, CreateRouteResource
)
from myapi.api.schemas import UserSchema

from myapi.utils import CipherHook

blueprint = Blueprint("api", __name__, url_prefix="/westhide/api")
api = Api(blueprint)

api.add_resource(RootPage, "/", endpoint="rootpage")
api.add_resource(UserResource, "/user", endpoint="api_user")
api.add_resource(UserList, "/userList", endpoint="api_userList")
api.add_resource(PermitCodeResource, "/permitCode", endpoint="api_role_permitCode")
api.add_resource(RouteResource, "/route", endpoint="api_route")
api.add_resource(CreateRouteResource, "/createRoute", endpoint="api_createRoute")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400


@blueprint.before_request
@jwt_required()
def before_request():
    return CipherHook().decryptRequest()


@blueprint.after_request
def after_request(response):
    return CipherHook().encryptResponse(response)
