from clickhouse_driver import connect
from flask import current_app as app


class Clickhouse():

    def __init__(self, config={
        "host": None, "port": None,
        "user": None, "password": None,
        "database": None
    }):
        self.config = config
        self.config["host"] = config["host"] or app.config.get("CLICKHOUSE_HOST")
        self.config["port"] = int(config["port"] or app.config.get("CLICKHOUSE_PORT"))
        self.config["user"] = config["user"] or app.config.get("CLICKHOUSE_USERNAME")
        self.config["password"] = config["password"] or app.config.get("CLICKHOUSE_PASSWORD")
        self.config["database"] = config["database"] or app.config.get("CLICKHOUSE_DATABASE")

    def make_connection(self):
        print(self.config)
        connection = connect(**self.config)
        return connection

    def execute(self, statement=''):
        if not (statement):
            return {'result': [], 'status': False, 'message': 'clickhouse语句为空！'}

        connection = self.make_connection()
        cursor = connection.cursor()

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
