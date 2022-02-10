from flask import jsonify, request
from flask_restful import Resource

from myapi.utils import Tenpay


class TenPayBillResource(Resource):
    @staticmethod
    def post():
        bill_date = request.json.get("billDate")

        result = Tenpay(bill_date).transfer_bill2db()

        return jsonify(result)
