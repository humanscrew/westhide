from flask import jsonify
from flask_restful import Resource

from myapi.collections import BookkeepingTemplate, FinanceVoucher
from myapi.api.schemas import BookkeepingTemplateSchema, FinanceVoucherSchema


class BookkeepingTemplateResource(Resource):

    def get(self):

        bookkeepingTemplateSchema = BookkeepingTemplateSchema()
        bookkeepingTemplate = BookkeepingTemplate.objects().all()

        return jsonify({"result": [bookkeepingTemplateSchema.dump(item) for item in bookkeepingTemplate]})
