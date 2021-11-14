from flask_restful import Resource, request

from myapi.utils import Tenpay


class TenPayResource(Resource):

    # def get(self):
    #
    #     if not request.args:
    #         return {"message": "请求参数不能为空"}, 405

    # smsQuery = AliyunSms().query(**request.args)
    # return jsonify(smsQuery)

    def post(self):
        result = Tenpay().transfer_bill2db("2021-11-10")
        return result
        # phoneNumbers = request.json.get("phoneNumbers")
        # if phoneNumbers:
        #     smsSend = AliyunSms().send(phoneNumbers)
        #     return jsonify(smsSend)
        # else:
        #     return {"message": "手机号不能为空"}, 405
