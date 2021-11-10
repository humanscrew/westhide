from clickhouse_driver import connect
from flask import current_app as app
import pandas


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
        connection = connect(**self.config)
        return connection

    def execute(self, statement=''):
        if not (statement):
            return {'result': [], 'code': 400, 'message': 'SQL语句为空！'}

        connection = self.make_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(statement)
            result = cursor.fetchall()
            columns = cursor.columns_with_types
            connection.commit()

            df = pandas.DataFrame(result, columns=[column[0] for column in columns])
            result = df.to_dict(orient='records')
            return {'result': result, 'code': 200, 'message': '数据库操作成功！'}
        except:
            connection.rollback()
            return {'result': [], 'code': 400, 'message': '数据库操作失败！'}
        finally:
            cursor.close()
            connection.close()
