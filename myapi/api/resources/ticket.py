from flask_restful import Resource, request

from myapi.models import TicketLaiu8, Laiu8Client
from myapi.api.schemas import TicketLaiu8Schema, Laiu8ClientSchema

from myapi.utils import HandleQuery


class TicketLaiu8Resource(Resource):

    def get(self):
        requestData = request.args
        sorter = requestData.get('sorter', [])
        filter = requestData.get('filterIn', [])

        ticketLaiu8 = HandleQuery(TicketLaiu8).sort(sorter).filterIn(filter)

        ticketLaiu8Schema = TicketLaiu8Schema(many=True)
        return ticketLaiu8.paginate(ticketLaiu8Schema)


class Laiu8ClientResource(Resource):

    def get(self):

        requestData = request.args
        sorter = requestData.get('sorter', [])
        filter = requestData.get('filterIn', [])

        laiu8Client = HandleQuery(Laiu8Client).sort(sorter).filterIn(filter)

        laiu8ClientSchema = Laiu8ClientSchema(many=True)
        return laiu8Client.paginate(laiu8ClientSchema)
