from flask import jsonify
from flask_restful import Resource, request

from myapi.models import SmsAliyun, SmsAliyunDetail
from myapi.api.schemas import SmsAliyunSchema, SmsAliyunDetailSchema

from myapi.utils import AliyunSms


class SmsAliyunResource(Resource):

    def get(self):

        if not request.args:
            return {"message": "请求参数不能为空"}, 405

        smsQuery = AliyunSms().query(**request.args)
        return jsonify(smsQuery)

    def post(self):

        phoneNumbers = request.json.get("phoneNumbers")
        if phoneNumbers:
            smsSend = AliyunSms().send(phoneNumbers)
            return jsonify(smsSend)
        else:
            return {"message": "手机号不能为空"}, 405
