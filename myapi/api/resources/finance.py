from flask_restful import Resource, request
from flask import jsonify

from myapi.collections import FinanceVoucher


class BookkeepingTemplateResource(Resource):

    def get(self):

        financeVoucher = FinanceVoucher.objects.all()
        return jsonify(financeVoucher)
        # return bookkeepingTemplate.paginate()
