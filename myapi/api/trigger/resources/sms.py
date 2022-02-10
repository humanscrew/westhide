from flask import jsonify, request
from flask_restful import Resource

from myapi.utils import AliyunSms


class SmsAliyunResource(Resource):
    @staticmethod
    def get():

        if not request.args:
            return {"message": "请求参数不能为空"}, 405

        sms_query = AliyunSms().query(**request.args)
        return jsonify(sms_query)

    @staticmethod
    def post():

        phone_numbers = request.json.get("phoneNumbers")
        if phone_numbers:
            sms_send = AliyunSms().send(phone_numbers)
            return jsonify(sms_send)
        else:
            return {"message": "手机号不能为空"}, 405
