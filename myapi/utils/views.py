from flask import Blueprint

from flask_restful import Api

from myapi.utils.sql import SQLResource
from myapi.utils.rsa import RSAResource


blueprint = Blueprint("utils", __name__, url_prefix="/westhide/utils")
api = Api(blueprint)

api.add_resource(SQLResource, "/sql", endpoint="utils_sql")
api.add_resource(RSAResource, "/rsa", endpoint="utils_rsa")
