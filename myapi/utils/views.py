from flask import Blueprint

from flask_restful import Api

from myapi.utils import RSAResource, DefaultRSAResource, SmsAliyunResource

blueprint = Blueprint("utils", __name__, url_prefix="/westhide/utils")
api = Api(blueprint)

api.add_resource(RSAResource, "/rsa", endpoint="utils_rsa")
api.add_resource(DefaultRSAResource, "/defaultRSA", endpoint="utils_defaultRSA")
api.add_resource(SmsAliyunResource, "/smsAliyun", endpoint="utils_smsAliyun")
