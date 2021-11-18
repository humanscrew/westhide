from flask import request, jsonify
from flask_restful import Resource

from myapi.utils import Tenpay


class TransferTenPayBillResource(Resource):
    @staticmethod
    def post():
        bill_date = request.json.get("billDate")
        result = Tenpay(bill_date).transfer_bill2db()

        return jsonify(result)
