from flask import jsonify
from flask_restful import Resource, request

from myapi.utils import HandleObjects

from myapi.collections import BookkeepingTemplate, FinanceVoucher
from myapi.api.schemas import BookkeepingTemplateSchema, FinanceVoucherSchema


class BookkeepingTemplateResource(Resource):

    def get(self):

        bookkeepingTemplateSchema = BookkeepingTemplateSchema(many=True)
        bookkeepingTemplate = HandleObjects(BookkeepingTemplate, bookkeepingTemplateSchema, request).deal()

        return jsonify(bookkeepingTemplate.paginate())


class FinanceVoucherResource(Resource):

    def get(self):

        financeVoucherSchema = FinanceVoucherSchema(many=True)
        financeVoucher = HandleObjects(FinanceVoucher, financeVoucherSchema, request).deal()

        return jsonify(financeVoucher.paginate())
