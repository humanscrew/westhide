from flask import Blueprint, request, jsonify
from flask_restful import Api

from marshmallow import ValidationError

from myapi.common import CipherHook

from .resources import (
    LoginResource,
    RegisterResource,
    RSAResource,
    DefaultRSAResource,
    SmsAliyunResource,
    TenPayBillResource,
)

blueprint = Blueprint("trigger", __name__, url_prefix="/westhide/trigger")
api = Api(blueprint)

api.add_resource(LoginResource, "/login", endpoint="trigger_login")
api.add_resource(RegisterResource, "/register", endpoint="trigger_register")
api.add_resource(RSAResource, "/RSA", endpoint="trigger_RSA")
api.add_resource(DefaultRSAResource, "/defaultRSA", endpoint="trigger_defaultRSA")
api.add_resource(SmsAliyunResource, "/smsAliyun", endpoint="trigger_smsAliyun")
api.add_resource(
    TenPayBillResource,
    "/tenPayBill",
    endpoint="trigger_tenPayBill",
)


# @blueprint.before_app_first_request
# def register_views():
#     apispec.spec.path(view=login, app=app)
#     apispec.spec.path(view=refresh, app=app)
#     apispec.spec.path(view=revoke_access_token, app=app)
#     apispec.spec.path(view=revoke_refresh_token, app=app)


@blueprint.before_request
def before_request():
    if request.method == "POST" and not request.is_json:
        return {"message": "Missing JSON in request"}, 405
    return CipherHook.decrypt_request()


@blueprint.after_request
def after_request(response):
    return CipherHook.encrypt_response(response)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
