from flask import jsonify, request
from flask_restful import Resource

from myapi.utils import Mysql


class MysqlResource(Resource):
    @staticmethod
    def post():
        request_data = request.json
        statement = request_data.get("statement")

        mysql = Mysql(config={**request_data})

        result = mysql.execute(statement)

        return jsonify({**result})
