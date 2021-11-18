from flask import Blueprint

from flask_restful import Api

from .resources import RSAResource, DefaultRSAResource, SmsAliyunResource

blueprint = Blueprint("trigger", __name__, url_prefix="/westhide/trigger")
api = Api(blueprint)

api.add_resource(RSAResource, "/rsa", endpoint="trigger_rsa")
api.add_resource(DefaultRSAResource, "/defaultRSA", endpoint="trigger_defaultRSA")
api.add_resource(SmsAliyunResource, "/smsAliyun", endpoint="trigger_smsAliyun")
