import pymysql
import os

from flask import request, jsonify

from flask_restful import Resource

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from myapi.utils.rsa import RSA
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
            return {'result': '', 'status': False, 'message': 'sql语句为空！'}
        try:
            connection = self.make_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            sqlresult = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            return {'result': sqlresult, 'status': True, 'message': '数据库操作成功！'}
        except:
            return {'result': '', 'status': False, 'message': '数据库操作失败！'}


class SQLResource(Resource):

    method_decorators = [jwt_required()]

    def post(self):
        requestData = request.json
        aesKeyWithRSA = requestData.get('aesKey')
        aesIVWithRSA = requestData.get('aesIV')
        sqlWithAES = requestData.get('sql')
        user_id = get_jwt_identity()
        sql, __aesKey, __aesIV = RSA().decryptWithRSA(sqlWithAES, aesKeyWithRSA, aesIVWithRSA, user_id)
        sqlresult = SQL().executeSQL(sql)
        sqlresultData = sqlresult.get('result')
        if sqlresultData:
            sqlresult["result"] = AES(__aesKey, __aesIV).encrypt(jsonify(sqlresultData))
        return jsonify(sqlresult)
