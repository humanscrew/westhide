import pymysql
import os


class SQL:

    def __init__(self, sqlConfig={
        "host": None, "port": None,
        "user": None, "password": None,
        "db": None, "charset": None
    }):
        self.sqlConfig = sqlConfig
        self.sqlConfig["host"] = sqlConfig["host"] or os.getenv("DATABASE_HOST")
        self.sqlConfig["port"] = int(sqlConfig["port"] or os.getenv("DATABASE_PORT"))
        self.sqlConfig["user"] = sqlConfig["user"] or os.getenv("DATABASE_USERNAME")
        self.sqlConfig["password"] = sqlConfig["password"] or os.getenv("DATABASE_PASSWORD")
        self.sqlConfig["db"] = sqlConfig["db"] or os.getenv("DATABASE_DATABASE")
        self.sqlConfig["charset"] = sqlConfig["charset"] or os.getenv("DATABASE_CHARSET")

    def make_connection(self):
        connection = pymysql.connect(**self.sqlConfig)
        return connection

    def executeSQL(self, sql=''):
        if not (sql):
            return {'result': [], 'status': False, 'message': 'sql语句为空！'}

        connection = self.make_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)  # pymysql.cursors.SSCursor

        try:
            cursor.execute(sql)
            sqlresult = cursor.fetchall()
            connection.commit()
            return {'result': sqlresult, 'status': True, 'message': '数据库操作成功！'}
        except:
            connection.rollback()
            return {'result': [], 'status': False, 'message': '数据库操作失败！'}
        finally:
            cursor.close()
            connection.close()
