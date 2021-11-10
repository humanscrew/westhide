from flask import jsonify
from flask_restful import Resource, request

from myapi.utils import Mysql


class MysqlResource(Resource):

    def post(self):

        requestData = request.json

        host = request.json.get('host')
        port = request.json.get('port')
        user = request.json.get('user')
        password = request.json.get('password')
        db = request.json.get('db')
        charset = request.json.get('charset')
        statement = requestData.get('statement')

        if not host and not user and not password and not db:
            mysql = Mysql(config={
                "host": host, "port": port,
                "user": user, "password": password,
                "db": db, "charset": charset
            })
        else:
            mysql = Mysql()

        result = mysql.execute(statement)
        return jsonify({**result})
