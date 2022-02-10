from flask import jsonify, request
from flask_restful import Resource

from myapi.utils import Clickhouse


class ClickhouseResource(Resource):
    @staticmethod
    def post():
        request_data = request.json
        statement = request_data.get("statement")

        clickhouse = Clickhouse(config={**request_data})

        result = clickhouse.execute(statement)

        return jsonify({**result})
