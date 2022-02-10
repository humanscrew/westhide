from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from celery import Celery
from flask_debugtoolbar import DebugToolbarExtension

from .common.apispec import APISpecExt
from .common.struct_timestamp import model_timestamp, document_timestamp
from .utils.database import ClickhouseSQLAlchemy
from .utils.logs import Logger

from sqlalchemy_bulk_lazy_loader import BulkLazyLoader

BulkLazyLoader.register_loader()

db = SQLAlchemy()
model_timestamp(db)
cdb = ClickhouseSQLAlchemy()
mdb = MongoEngine()
document_timestamp(mdb)
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
apispec = APISpecExt()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
celery = Celery()
toolbar = DebugToolbarExtension()

logger = Logger()
