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
from myapi.utils import RSA, CipherHook
from myapi.api.schemas import UserSchema
from marshmallow import INCLUDE, ValidationError

blueprint = Blueprint("auth", __name__, url_prefix="/westhide/auth")


@blueprint.route("/login", methods=["POST"])
def login():
    """Authenticate user and return tokens

    ---
    post:
      tags:
        - auth
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: myUser
                  required: true
                password:
                  type: string
                  example: P4$$w0rd!
                  required: true
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myAccessToken
                  refresh_token:
                    type: string
                    example: myRefreshToken
        400:
          description: bad request
      security: []
    """
    if not request.is_json:
        return {"message": "Missing JSON in request"}, 405

    requestData = request.json
    username = requestData.get("username", None)
    passwordWithAES = requestData.get("password", None)
    if not username or not passwordWithAES:
        return {"message": "Missing username or password"}, 401

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"message": "用户名错误"}, 401

    user_id = user.id
    aesKeyWithRSA = request.headers.get('aesKey', None)
    aesIVWithRSA = request.headers.get("aesIV", None)
    if not aesKeyWithRSA or not aesIVWithRSA:
        return {"message": "请求密钥缺失"}, 400
    password,  g.aesKey, g.aesIV = RSA().decryptWithRSA(passwordWithAES, aesKeyWithRSA, aesIVWithRSA, user_id)

    if not pwd_context.verify(password, user.password):
        return {"message": "密码错误"}, 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    ret = {"accessToken": access_token, "refreshToken": refresh_token, "message": "登录成功"}
    return ret


@blueprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return {"message": "Missing JSON in request"}, 405

    requestData = request.json
    username = requestData.pop('username', None)
    if username and User.query.with_entities(User.id).filter_by(username=username).first():
        return {"message": "该用户名已被注册"}, 400
    mobile = requestData.get('mobile')
    if mobile and User.query.with_entities(User.id).filter_by(mobile=mobile).first():
        return {"message": "该手机号已被注册"}, 400
    email = requestData.get('email')
    if email and User.query.with_entities(User.id).filter_by(email=email).first():
        return {"message": "该邮箱已被注册"}, 400

    defaultPrivateKey = RSA().getDefaultRSA().get("privateKey")
    CipherHook().decryptRequest(None, defaultPrivateKey)

    requestData.update(username=username)
    userSchema = UserSchema(unknown=INCLUDE)
    user = userSchema.load(requestData)
    db.session.add(user)
    db.session.commit()
    return {**userSchema.dump(user), "message": "注册成功"}, 201


@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Get an access token from a refresh token

    ---
    post:
      tags:
        - auth
      parameters:
        - in: header
          name: Authorization
          required: true
          description: valid refresh token
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myAccessToken
        400:
          description: bad request
        401:
          description: unauthorized
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"accessToken": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return ret


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    """Revoke an access token

    ---
    delete:
      tags:
        - auth
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return {"message": "token revoked"}


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    """Revoke a refresh token, used mainly for logout

    ---
    delete:
      tags:
        - auth
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
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
    return CipherHook().encryptResponse(response)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
