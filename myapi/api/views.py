from flask import Blueprint, current_app, jsonify, request
from flask_restful import Api
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from marshmallow import ValidationError
from myapi.extensions import apispec
from myapi.api.resources import UserResource, UserList, RootPage
from myapi.api.schemas import UserSchema
from myapi.utils.rsa import RSA
from myapi.utils.aes import encryptResponse


blueprint = Blueprint("api", __name__, url_prefix="/westhide/api")
api = Api(blueprint)

api.add_resource(RootPage, "/", endpoint="rootpage")
api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")


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
    if not request.is_json:
        return None
    requestData = request.json
    aesKeyWithRSA = requestData.get("aesKey")
    aesKeyWithIV = requestData.get("aesIV")
    if not aesKeyWithRSA or not aesKeyWithIV or not requestData:
        return None
    user_id = get_jwt_identity()
    requestData, __aesKey, __aesIV = RSA().decryptWithRSA(requestData, aesKeyWithRSA, aesKeyWithIV, user_id)
    requestData.update(aesKey=__aesKey, aesIV=__aesIV)
    return None


@blueprint.after_request
def after_request(response):
    return encryptResponse(response)
