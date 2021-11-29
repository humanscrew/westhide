from clickhouse_driver import connect
from myapi.config import CLICKHOUSE_SETTINGS, CLICKHOUSE_DATABASE_URI
import pandas

from sqlalchemy import create_engine, MetaData
from clickhouse_sqlalchemy import make_session, get_declarative_base


class Clickhouse:
    def __init__(self, config=None):
        if config is None:
            config = {
                "host": None,
                "port": None,
                "user": None,
                "password": None,
                "database": None,
                "compression": None,
            }
        self.config = config
        self.config["host"] = config["host"] or CLICKHOUSE_SETTINGS.get("host")
        self.config["port"] = config["port"] or CLICKHOUSE_SETTINGS.get("port")
        self.config["user"] = config["user"] or CLICKHOUSE_SETTINGS.get("username")
        self.config["password"] = config["password"] or CLICKHOUSE_SETTINGS.get(
            "password"
        )
        self.config["database"] = config["database"] or CLICKHOUSE_SETTINGS.get(
            "database"
        )
        self.config["compression"] = config["compression"] or CLICKHOUSE_SETTINGS.get(
            "compression"
        )

    def make_connection(self):
        connection = connect(**self.config)
        return connection

    def execute(self, statement=""):
        if not statement:
            return {"result": [], "code": 400, "message": "SQL语句为空！"}

        connection = self.make_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(statement)
            result = cursor.fetchall()
            columns = cursor.columns_with_types
            connection.commit()

            df = pandas.DataFrame(result, columns=[column[0] for column in columns])
            result = df.to_dict(orient="records")
            return {"result": result, "code": 200, "message": "数据库操作成功！"}
        except:
            connection.rollback()
            return {"result": [], "code": 400, "message": "数据库操作失败！"}
        finally:
            cursor.close()
            connection.close()


class ClickhouseSQLAlchemy:
    def __init__(self):
        engine = create_engine(CLICKHOUSE_DATABASE_URI)
        metadata = MetaData(bind=engine)
        self.session = make_session(engine)
        self.Model = get_declarative_base(metadata=metadata)
