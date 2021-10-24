from myapi.extensions import ma, db
from myapi.models import TicketLaiu8, TicketLaiu8Refund, Laiu8Client, Ticket2Finance


class TicketLaiu8RefundSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = TicketLaiu8Refund
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)


class TicketLaiu8Schema(ma.SQLAlchemyAutoSchema):

    ticket_laiu8_refund = ma.Nested(TicketLaiu8RefundSchema, many=True)

    class Meta:
        model = TicketLaiu8
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)


class Laiu8ClientSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Laiu8Client
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)


class Ticket2FinanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket2Finance
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)
