from flask import request
from flask_restful import Resource

from myapi.utils import RSA
from myapi.struct.models import DefaultRSAModel
from myapi.struct.schemas import DefaultRSASchema


class RSAResource(Resource):
    @staticmethod
    def post():
        if not request.is_json:
            return {"message": "Missing JSON in request"}, 405

        username = request.json.get("username")
        if not username:
            return {"message": "用户名为空"}, 400

        public_key = RSA().set_rsa_key(username)
        if not public_key:
            return {"message": "用户名错误"}, 400

        return {"publicKey": public_key}


class DefaultRSAResource(Resource):
    @staticmethod
    def get():
        default_rsa_schema = DefaultRSASchema(only=("public_key",))
        default_rsa = DefaultRSAModel.query.first_or_404()

        return {**default_rsa_schema.dump(default_rsa)}
