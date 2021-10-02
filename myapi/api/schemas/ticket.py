from myapi.extensions import ma, db
from myapi.models import TicketLaiu8, TicketLaiu8Refund


class TicketLaiu8RefundSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = TicketLaiu8Refund
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)


class TicketLaiu8Schema(ma.SQLAlchemyAutoSchema):

    ticket_laiu8_refund = ma.Nested(TicketLaiu8RefundSchema, many=True, data_key="ticket_laiu8_refund")

    class Meta:
        model = TicketLaiu8
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)
