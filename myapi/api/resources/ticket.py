from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from myapi.models import TicketLaiu8
from myapi.api.schemas import TicketLaiu8Schema

from sqlalchemy.sql.expression import and_

import time


class TicketLaiu8Resource(Resource):

    def get(self):
        parser = RequestParser()
        parser.add_argument('startTime')
        parser.add_argument('endTime')
        args = parser.parse_args()

        startTime = time.strptime(args.startTime, "%Y-%m-%d  %H:%M:%S")
        endTime = time.strptime(args.endTime, "%Y-%m-%d %H:%M:%S")

        ticketLaiu8 = TicketLaiu8.query.filter(
            and_(
                TicketLaiu8.departure_datetime >= startTime,
                TicketLaiu8.departure_datetime <= endTime
            )
        ).all()

        ticketLaiu8Schema = TicketLaiu8Schema(many=True)
        ticketLaiu8 = ticketLaiu8Schema.dump(ticketLaiu8)
        return {"ticketLaiu8": ticketLaiu8}
