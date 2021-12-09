"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from celery import Celery
from flask_debugtoolbar import DebugToolbarExtension

from .commons.apispec import APISpecExt
from .commons.lib import Lib

from .utils.database import ClickhouseSQLAlchemy

from .logs import Logger

from sqlalchemy_bulk_lazy_loader import BulkLazyLoader

BulkLazyLoader.register_loader()

db = SQLAlchemy()
cdb = ClickhouseSQLAlchemy()
mdb = MongoEngine()
jwt = JWTManager()
ma = Marshmallow()
ma.SQLAlchemyAutoSchema.on_bind_field = Lib.camel_case

migrate = Migrate()
apispec = APISpecExt()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
celery = Celery()
toolbar = DebugToolbarExtension()

logger = Logger()
