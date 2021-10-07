from flask_restful import Resource, request
from flask_restful.reqparse import RequestParser

from myapi.commons.pagination import paginate
from myapi.models import TicketLaiu8, Laiu8Client
from myapi.api.schemas import TicketLaiu8Schema, Laiu8ClientSchema

from myapi.utils import Lib


class TicketLaiu8Resource(Resource):

    def get(self):
        requestData = request.args
        sortName = requestData.pop('field', None)
        order = requestData.pop('order', None)

        columns = TicketLaiu8.__table__.columns.keys()

        sortColumnName = Lib.camel2UnderScore(sortName) if sortName else None
        if sortColumnName in columns and order:
            ticketLaiu8 = TicketLaiu8.query.order_by(getattr(getattr(TicketLaiu8, sortColumnName), order)())
        else:
            # ticketLaiu8 = TicketLaiu8.query.order_by(TicketLaiu8.is_lock.desc(), TicketLaiu8.create_time.desc())
            ticketLaiu8 = TicketLaiu8.query

        for key in requestData:
            filterColumnName = Lib.camel2UnderScore(key)
            filterItems = requestData[key]
            if filterColumnName in columns and filterItems:
                ticketLaiu8 = ticketLaiu8.filter(getattr(TicketLaiu8, filterColumnName).in_(filterItems))

        ticketLaiu8Schema = TicketLaiu8Schema(many=True)
        return paginate(ticketLaiu8, ticketLaiu8Schema)


class Laiu8ClientResource(Resource):

    def get(self):
        requestData = request.args
        sortName = requestData.pop('field', None)
        order = requestData.pop('order', None)

        columns = Laiu8Client.__table__.columns.keys()

        sortColumnName = Lib.camel2UnderScore(sortName) if sortName else None
        if sortColumnName in columns and order:
            laiu8Client = Laiu8Client.query.order_by(getattr(getattr(Laiu8Client, sortColumnName), order)())
        else:
            laiu8Client = Laiu8Client.query.order_by(Laiu8Client.sales.desc())

        for key in requestData:
            filterColumnName = Lib.camel2UnderScore(key)
            filterItems = requestData[key]
            if filterColumnName in columns and filterItems:
                laiu8Client = laiu8Client.filter(getattr(Laiu8Client, filterColumnName).in_(filterItems))

        laiu8ClientSchema = Laiu8ClientSchema(many=True)
        return paginate(laiu8Client, laiu8ClientSchema)
