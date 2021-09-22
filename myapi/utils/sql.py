import pymysql
import os

from flask import request, jsonify

from flask_restful import Resource

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from myapi.utils.aes import AES


class SQL:
    def make_connection(self):
        connection = pymysql.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USERNAME"),
            password=os.getenv("DATABASE_PASSWORD"),
            db=os.getenv("DATABASE_DATABASE"),
            charset=os.getenv("DATABASE_CHARSET")
        )
        return connection

    def executeSQL(self, sql=''):
        if not (sql):
            return {'data': '', 'status': False, 'message': 'sql语句为空！'}
        try:
            connection = self.make_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            sqlresult = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            return {'data': sqlresult, 'status': True, 'message': '数据库操作成功！'}
        except:
            return {'data': '', 'status': False, 'message': '数据库操作失败！'}


class SQLResource(Resource):

    method_decorators = [jwt_required()]

    def post(self):
        requestData = request.json
        aesKeyWithRSA = requestData.get('aesKey')
        sqlWithAES = requestData.get('sql')
        user_id = get_jwt_identity()
        sql, _aesKey = AES().decryptWithRSA(sqlWithAES, aesKeyWithRSA, user_id)
        sqlresult = SQL().executeSQL(sql)
        sqlresultData = sqlresult.get('data')
        if sqlresultData:
            sqlresult["data"] = AES().encrypt(jsonify(sqlresultData), _aesKey)
        return jsonify(sqlresult)
