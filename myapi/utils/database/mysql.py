import pymysql
from myapi.config import MYSQL_SETTINGS


class Mysql:
    def __init__(self, config=None):
        if config is None:
            config = {}

        self.config = {
            key: config.get(key) or value
            for key, value in MYSQL_SETTINGS.items()
            if key not in ["dialect", "driver"]
        }

    def make_connection(self):
        connection = pymysql.connect(**self.config)
        return connection

    def execute(self, statement=""):
        if not statement:
            return {"result": [], "code": 400, "message": "SQL语句为空！"}

        connection = self.make_connection()
        cursor = connection.cursor(
            pymysql.cursors.DictCursor
        )  # pymysql.cursors.SSCursor

        try:
            cursor.execute(statement)
            result = cursor.fetchall()
            connection.commit()
            return {"result": result, "code": 200, "message": "数据库操作成功！"}
        except:
            connection.rollback()
            return {"result": [], "code": 400, "message": "数据库操作失败！"}
        finally:
            cursor.close()
            connection.close()
