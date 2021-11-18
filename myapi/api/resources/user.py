from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from myapi.schemas import UserSchema
from myapi.models import User
from myapi.commons import HandleQuery

from myapi.extensions import db


class UserResource(Resource):
    @staticmethod
    def get():
        user_schema = UserSchema()
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        return {**user_schema.dump(user)}

    @staticmethod
    def post():
        user_schema = UserSchema()
        user = user_schema.load(request.json)

        db.session.add(user)
        db.session.commit()

        return {**user_schema.dump(user), "message": "user created"}, 201

    @staticmethod
    def put():
        user_schema = UserSchema(partial=True)
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        user = user_schema.load(request.json, instance=user)

        db.session.commit()

        return {"user": user_schema.dump(user), "message": "user updated"}

    @staticmethod
    def delete():
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "user deleted"}


class UserListResource(Resource):
    @staticmethod
    def get():
        user_schema = UserSchema(many=True)
        user = HandleQuery(User, user_schema, request).deal()

        return user.paginate()
