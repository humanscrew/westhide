from flask_restful import Resource, request

from myapi.models import TicketLaiu8, Laiu8Client
from myapi.api.schemas import TicketLaiu8Schema, Laiu8ClientSchema

from myapi.utils import HandleQuery


class TicketLaiu8Resource(Resource):

    def get(self):
        requestData = request.args
        sorter = requestData.get('sorter', [])
        filterIn = requestData.get('filterIn', [])
        filterLike = requestData.get('filterLike', [])
        withEntities = requestData.get('withEntities', [])
        distinct = requestData.get('distinct', [])
        limit = requestData.get('limit', [])
        offset = requestData.get('offset', [])

        ticketLaiu8Schema = TicketLaiu8Schema(many=True)
        ticketLaiu8 = HandleQuery(TicketLaiu8, ticketLaiu8Schema).deal(
            sorter, filterIn, filterLike, withEntities, distinct, limit, offset
        )

        return ticketLaiu8.paginate()


class Laiu8ClientResource(Resource):

    def get(self):

        requestData = request.args
        sorter = requestData.get('sorter', [])
        filterIn = requestData.get('filterIn', [])
        filterLike = requestData.get('filterLike', [])
        withEntities = requestData.get('withEntities', [])
        distinct = requestData.get('distinct', [])
        limit = requestData.get('limit', [])
        offset = requestData.get('offset', [])

        laiu8ClientSchema = Laiu8ClientSchema(many=True)
        laiu8Client = HandleQuery(Laiu8Client, laiu8ClientSchema).deal(
            sorter, filterIn, filterLike, withEntities, distinct, limit, offset
        )

        return laiu8Client.paginate()
