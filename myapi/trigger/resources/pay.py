from flask_restful import Resource


class TenPayTrigger(Resource):
    @staticmethod
    def post():
        bill_date = request.json.get("billDate")

        result = Tenpay(bill_date).transfer_bill2db()

        return jsonify(result)
