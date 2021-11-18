from flask import jsonify, request
from flask_restful import Resource

from myapi.utils import Clickhouse


class ClickhouseResource(Resource):

    @staticmethod
    def post():
        request_data = request.json
        host = request.json.get('host')
        port = request.json.get('port')
        user = request.json.get('user')
        password = request.json.get('password')
        database = request.json.get('database')
        statement = request_data.get('statement')

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
