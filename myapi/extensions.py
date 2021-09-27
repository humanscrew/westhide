"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from celery import Celery

from myapi.commons.apispec import APISpecExt


db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
apispec = APISpecExt()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
celery = Celery()


def camelCase(self, field_name, field_obj):
    string = field_obj.data_key or field_name
    parts = iter(string.split("_"))
    field_obj.data_key = next(parts) + "".join(item.title() for item in parts)


ma.SQLAlchemyAutoSchema.on_bind_field = camelCase
