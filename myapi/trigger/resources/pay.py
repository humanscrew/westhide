from flask import request, jsonify
from flask_restful import Resource

from myapi.utils import Tenpay


class TenPayBillResource(Resource):
    @staticmethod
    def post():
        platform = request.json.get("platform")
        bill_date = request.json.get("billDate")

        if isinstance(platform, str):
            result = Tenpay(platform, bill_date).transfer_bill2db()
        elif isinstance(platform, list):
            result = [Tenpay(item, bill_date).transfer_bill2db() for item in platform]
        else:
            return {"message": "Please post the correct platform"}, 400
        return jsonify(result)
