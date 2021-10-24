from flask_restful import Resource, request

from myapi.models import TicketLaiu8, Laiu8Client, Ticket2Finance
from myapi.api.schemas import TicketLaiu8Schema, Laiu8ClientSchema, Ticket2FinanceSchema

from myapi.utils import HandleQuery


class TicketLaiu8Resource(Resource):

    def get(self):

        ticketLaiu8Schema = TicketLaiu8Schema(many=True)
        ticketLaiu8 = HandleQuery(TicketLaiu8, ticketLaiu8Schema, request).deal()

        return ticketLaiu8.paginate()


class Laiu8ClientResource(Resource):

    def get(self):

        laiu8ClientSchema = Laiu8ClientSchema(many=True)
        laiu8Client = HandleQuery(Laiu8Client, laiu8ClientSchema, request).deal()

        return laiu8Client.paginate()


class Ticket2FinanceResource(Resource):

    def get(self):

        ticket2FinanceSchema = Ticket2FinanceSchema(many=True)
        ticket2Finance = HandleQuery(Ticket2Finance, ticket2FinanceSchema, request).deal()

        return ticket2Finance.paginate()
