from flask import jsonify, request
from flask_restful import Resource

from myapi.utils import Tenpay


class TenPayBillResource(Resource):

    # def get(self):
    #
    #     if not request.args:
    #         return {"message": "请求参数不能为空"}, 405

    # smsQuery = AliyunSms().query(**request.args)
    # return jsonify(smsQuery)

    @staticmethod
    def post():
        bill_date = request.json.get("billDate")

        result = Tenpay(bill_date).transfer_bill2db()

        return jsonify(result)
