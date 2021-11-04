import pymysql
from flask import current_app as app


class Mysql:

    def __init__(self, config={
        "host": None, "port": None,
        "user": None, "password": None,
        "db": None, "charset": None
    }):
        self.config = config
        self.config["host"] = config["host"] or app.config.get("DATABASE_HOST")
        self.config["port"] = int(config["port"] or app.config.get("DATABASE_PORT"))
        self.config["user"] = config["user"] or app.config.get("DATABASE_USERNAME")
        self.config["password"] = config["password"] or app.config.get("DATABASE_PASSWORD")
        self.config["db"] = config["db"] or app.config.get("DATABASE_DATABASE")
        self.config["charset"] = config["charset"] or app.config.get("DATABASE_CHARSET")

    def make_connection(self):
        connection = pymysql.connect(**self.config)
        return connection

    def execute(self, statement=''):
        if not (statement):
            return {'result': [], 'status': False, 'message': 'sql语句为空！'}

        connection = self.make_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)  # pymysql.cursors.SSCursor

        try:
            cursor.execute(statement)
            result = cursor.fetchall()
            connection.commit()
            return {'result': result, 'status': True, 'message': '数据库操作成功！'}
        except:
            connection.rollback()
            return {'result': [], 'status': False, 'message': '数据库操作失败！'}
        finally:
            cursor.close()
            connection.close()
