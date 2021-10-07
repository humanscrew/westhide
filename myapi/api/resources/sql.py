from flask import jsonify
from flask_restful import Resource, request

from myapi.utils import SQL


class SQLResource(Resource):

    def post(self):
        if not request.is_json:
            return {"message": "Missing JSON in request"}, 405

        requestData = request.json

        host = request.json.get('host')
        port = request.json.get('port')
        user = request.json.get('user')
        password = request.json.get('password')
        db = request.json.get('db')
        charset = request.json.get('charset')
        sqlStatement = requestData.get('sqlStatement')

        if not host and not user and not password and not db:
            sqlInstance = SQL(sqlConfig={
                "host": host, "port": port,
                "user": user, "password": password,
                "db": db, "charset": charset
            })
        else:
            sqlInstance = SQL()

        sqlresult = sqlInstance.executeSQL(sqlStatement)
        return jsonify({**sqlresult})
