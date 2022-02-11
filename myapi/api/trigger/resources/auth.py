from flask import request, current_app as app
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)

from myapi.common.token import is_token_revoked, add_token_to_database

from myapi.struct.models import User
from myapi.extensions import pwd_context, jwt, db
from myapi.utils import AliyunSms
from myapi.struct.schemas import UserSchema


class LoginResource(Resource):
    @staticmethod
    def post():

        request_data = request.json
        username = request_data.get("username", None)
        password = request_data.get("password", None)
        if not username or not password:
            return {"message": "Missing username or password"}, 401

        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "用户名错误"}, 400

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


class RegisterResource(Resource):
    @staticmethod
    def post():

        request_data = request.json
        username = request_data.pop("username", None)

        if (
            username
            and User.query.with_entities(User.id).filter_by(username=username).first()
        ):
            return {"message": "该用户名已被注册"}, 400

        mobile = request_data.get("mobile")
        if (
            mobile
            and User.query.with_entities(User.id).filter_by(mobile=mobile).first()
        ):
            return {"message": "该手机号已被注册"}, 400

        email = request_data.get("email")
        if email and User.query.with_entities(User.id).filter_by(email=email).first():
            return {"message": "该邮箱已被注册"}, 400

        sms = request_data.get("sms")
        aliyun_sms = AliyunSms().query(**sms.get("callback"))
        if not sms.get("code") == aliyun_sms["result"]["params"]["code"]:
            return {"message": "验证码错误"}, 400

        user_schema = UserSchema(unknown=INCLUDE)
        user = user_schema.load(request_data)
        db.session.add(user)
        db.session.commit()
        return {**user_schema.dump(user), "message": "注册成功"}, 201


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    identity = jwt_payload["sub"]
    return User.query.get(identity)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_payload)


# @jwt_required(refresh=True)
# def refresh():
#     current_user = get_jwt_identity()
#     access_token = create_access_token(identity=current_user)
#     ret = {"accessToken": access_token}
#     add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
#     return ret
#
#
# @jwt_required()
# def revoke_access_token():
#     jti = get_jwt()["jti"]
#     user_identity = get_jwt_identity()
#     revoke_token(jti, user_identity)
#     return {"message": "token revoked"}
#
#
# @jwt_required(refresh=True)
# def revoke_refresh_token():
#     jti = get_jwt()["jti"]
#     user_identity = get_jwt_identity()
#     revoke_token(jti, user_identity)
#     return {"message": "token revoked"}
