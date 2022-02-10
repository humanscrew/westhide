from flask import jsonify, request
from flask_restful import Resource

from myapi.common import HandleObjects

from myapi.struct.collections import BookkeepingTemplate, FinanceVoucher
from myapi.struct.schemas import BookkeepingTemplateSchema, FinanceVoucherSchema


class BookkeepingTemplateResource(Resource):
    @staticmethod
    def get():
        bookkeeping_template_schema = BookkeepingTemplateSchema(many=True)
        bookkeeping_template = HandleObjects(
            BookkeepingTemplate, bookkeeping_template_schema, request
        ).deal()

        return jsonify(bookkeeping_template.paginate())


class FinanceVoucherResource(Resource):
    @staticmethod
    def get():
        finance_voucher_schema = FinanceVoucherSchema(many=True)
        finance_voucher = HandleObjects(
            FinanceVoucher, finance_voucher_schema, request
        ).deal()

        return jsonify(finance_voucher.paginate())
