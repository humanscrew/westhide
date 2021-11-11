import pymysql
from myapi.config import MYSQL_SETTINGS


class Mysql:

    def __init__(self, config={
        "host": None, "port": None,
        "user": None, "password": None,
        "db": None, "charset": None
    }):
        self.config = config
        self.config["host"] = config["host"] or MYSQL_SETTINGS.get("host")
        self.config["port"] = int(config["port"] or MYSQL_SETTINGS.get("port"))
        self.config["user"] = config["user"] or MYSQL_SETTINGS.get("username")
        self.config["password"] = config["password"] or MYSQL_SETTINGS.get("password")
        self.config["db"] = config["db"] or MYSQL_SETTINGS.get("db")
        self.config["charset"] = config["charset"] or MYSQL_SETTINGS.get("charset")

    def make_connection(self):
        connection = pymysql.connect(**self.config)
        return connection

    def execute(self, statement=''):
        if not (statement):
            return {'result': [], 'code': 400, 'message': 'SQL语句为空！'}

        connection = self.make_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)  # pymysql.cursors.SSCursor

        try:
            cursor.execute(statement)
            result = cursor.fetchall()
            connection.commit()
            return {'result': result, 'code': 200, 'message': '数据库操作成功！'}
        except:
            connection.rollback()
            return {'result': [], 'code': 400, 'message': '数据库操作失败！'}
        finally:
            cursor.close()
            connection.close()
