from flask import request
from flask_restful import Resource

from myapi.struct.models import TicketLaiu8, Laiu8Client, Ticket2Finance
from myapi.struct.schemas import (
    TicketLaiu8Schema,
    Laiu8ClientSchema,
    Ticket2FinanceSchema,
)

from myapi.common import HandleQuery


class TicketLaiu8Resource(Resource):
    @staticmethod
    def get():
        ticket_laiu8_schema = TicketLaiu8Schema(many=True)
        ticket_laiu8 = HandleQuery(TicketLaiu8, ticket_laiu8_schema, request).deal()

        return ticket_laiu8.paginate()


class Laiu8ClientResource(Resource):
    @staticmethod
    def get():
        laiu8_client_schema = Laiu8ClientSchema(many=True)
        laiu8_client = HandleQuery(Laiu8Client, laiu8_client_schema, request).deal()

        return laiu8_client.paginate()


class Ticket2FinanceResource(Resource):
    @staticmethod
    def get():
        ticket2finance_schema = Ticket2FinanceSchema(many=True)
        ticket2finance = HandleQuery(
            Ticket2Finance, ticket2finance_schema, request
        ).deal()

        return ticket2finance.paginate()
