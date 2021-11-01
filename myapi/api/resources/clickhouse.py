from flask import jsonify
from flask_restful import Resource, request

from myapi.utils import Clickhouse


class ClickhouseResource(Resource):

    def post(self):
        if not request.is_json:
            return {"message": "Missing JSON in request"}, 405

        requestData = request.json

        host = request.json.get('host')
        port = request.json.get('port')
        user = request.json.get('user')
        password = request.json.get('password')
        database = request.json.get('database')
        statement = requestData.get('statement')

        if not host and not user and not password and not database:
            clickhouse = Clickhouse(config={
                "host": host, "port": port,
                "user": user, "password": password,
                "database": database
            })
        else:
            clickhouse = Clickhouse()

        result = clickhouse.execute(statement)
        return jsonify({**result})
