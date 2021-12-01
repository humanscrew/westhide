from flask import request, g, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from myapi.models import User
from myapi.extensions import pwd_context, jwt, apispec, db
from myapi.auth.helpers import revoke_token, is_token_revoked, add_token_to_database
from myapi.commons import CipherHook
from myapi.utils import RSA, AliyunSms
from myapi.schemas import UserSchema
from marshmallow import INCLUDE, ValidationError

blueprint = Blueprint("auth", __name__, url_prefix="/westhide/auth")


@blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return {"message": "Missing JSON in request"}, 405

    request_data = request.json
    username = request_data.get("username", None)
    password_with_aes = request_data.get("password", None)
    if not username or not password_with_aes:
        return {"message": "Missing username or password"}, 401

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"message": "用户名错误"}, 400

    user_id = user.id
    aes_key_with_rsa = request.headers.get("aesKey", None)
    aes_iv_with_rsa = request.headers.get("aesIV", None)
    if not aes_key_with_rsa or not aes_iv_with_rsa:
        return {"message": "请求密钥缺失"}, 400
    password, g.aesKey, g.aesIV = RSA().decrypt_with_rsa(
        password_with_aes, aes_key_with_rsa, aes_iv_with_rsa, user_id
    )

    if not pwd_context.verify(password, user.password):
        return {"message": "密码错误"}, 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "message": "登录成功",
    }


@blueprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return {"message": "Missing JSON in request"}, 405

    request_data = request.json
    username = request_data.pop("username", None)

    default_private_key = RSA().get_default_rsa().get("privateKey")
    CipherHook().decrypt_request(None, default_private_key)

    if (
        username
        and User.query.with_entities(User.id).filter_by(username=username).first()
    ):
        return {"message": "该用户名已被注册"}, 400

    mobile = request_data.get("mobile")
    if mobile and User.query.with_entities(User.id).filter_by(mobile=mobile).first():
        return {"message": "该手机号已被注册"}, 400

    email = request_data.get("email")
    if email and User.query.with_entities(User.id).filter_by(email=email).first():
        return {"message": "该邮箱已被注册"}, 400

    sms = request_data.get("sms")
    aliyun_sms = AliyunSms().query(**sms.get("callback"))
    if not sms.get("code") == aliyun_sms["result"]["params"]["code"]:
        return {"message": "验证码错误"}, 400

    request_data.update(username=username)
    user_schema = UserSchema(unknown=INCLUDE)
    user = user_schema.load(request_data)
    db.session.add(user)
    db.session.commit()
    return {**user_schema.dump(user), "message": "注册成功"}, 201


@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"accessToken": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return ret


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return {"message": "token revoked"}


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return {"message": "token revoked"}


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    identity = jwt_payload["sub"]
    return User.query.get(identity)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_payload)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=login, app=app)
    apispec.spec.path(view=refresh, app=app)
    apispec.spec.path(view=revoke_access_token, app=app)
    apispec.spec.path(view=revoke_refresh_token, app=app)


@blueprint.after_request
def after_request(response):
    return CipherHook.encrypt_response(response)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
