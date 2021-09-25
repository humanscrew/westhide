from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from myapi.api.schemas import UserSchema
from myapi.models import User
from myapi.extensions import db
from myapi.commons.pagination import paginate


class UserResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: user updated
                  user: UserSchema
        404:
          description: user does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: user deleted
        404:
          description: user does not exists
    """

    # method_decorators = [jwt_required()]

    def get(self):
        schema = UserSchema()
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return {"user": schema.dump(user)}

    def put(self):
        schema = UserSchema(partial=True)
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)

        db.session.commit()

        return {"message": "user updated", "user": schema.dump(user)}

    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "user deleted"}


class UserList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: user created
                  user: UserSchema
    """

    # method_decorators = [jwt_required()]

    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)

        db.session.add(user)
        db.session.commit()

        return {"message": "user created", "user": schema.dump(user)}, 201
