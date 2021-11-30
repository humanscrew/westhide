from graphene import ObjectType, types
from sqlalchemy import func, and_
from myapi.extensions import cdb
from myapi.models import TicketLaiu8CK
from datetime import datetime


class GrowCardType(ObjectType):
    visits = types.Int(
        product_type=types.List(types.String, default_value=["船票"]),
        ticket_status=types.List(types.String, default_value=["出票成功", "一检", "二检"]),
        start_time=types.String(
            default_value=datetime(datetime.now().year, datetime.now().month, 1)
        ),
        end_time=types.String(default_value=datetime.now()),
    )
    pre_sale_ticket = visits
    sales = types.Decimal(
        product_type=types.List(types.String, default_value=["船票"]),
        ticket_status=types.List(types.String, default_value=["出票成功", "一检", "二检"]),
        start_time=types.String(
            default_value=datetime(datetime.now().year, datetime.now().month, 1)
        ),
        end_time=types.String(default_value=datetime.now()),
    )
    net_cashflow = types.Decimal(
        product_type=types.List(types.String, default_value=["船票"]),
        start_time=types.String(
            default_value=datetime(datetime.now().year, datetime.now().month, 1)
        ),
        end_time=types.String(default_value=datetime.now()),
    )

    @staticmethod
    def resolve_visits(self, info, product_type, ticket_status, start_time, end_time):
        visits = (
            cdb.session.query(func.count(TicketLaiu8CK.id))
            .filter(
                and_(
                    TicketLaiu8CK.departure_datetime >= start_time,
                    TicketLaiu8CK.departure_datetime <= end_time,
                    TicketLaiu8CK.product_type.in_(product_type),
                    TicketLaiu8CK.ticket_status.in_(ticket_status),
                    func.if_(
                        TicketLaiu8CK.change_type.is_(None),
                        "",
                        TicketLaiu8CK.change_type,
                    )
                    != "已换船",
                )
            )
            .scalar()
        )
        return visits

    def resolve_pre_sale_ticket(self, *args, **kwargs):
        return self.resolve_visits(self, *args, **kwargs)

    @staticmethod
    def resolve_sales(self, info, product_type, ticket_status, start_time, end_time):
        sales = (
            cdb.session.query(func.sum(TicketLaiu8CK.ticket_price))
            .filter(
                and_(
                    TicketLaiu8CK.departure_datetime >= start_time,
                    TicketLaiu8CK.departure_datetime <= end_time,
                    TicketLaiu8CK.product_type.in_(product_type),
                    TicketLaiu8CK.ticket_status.in_(ticket_status),
                    func.if_(
                        TicketLaiu8CK.change_type.is_(None),
                        "",
                        TicketLaiu8CK.change_type,
                    )
                    != "已换船",
                )
            )
            .scalar()
        )

        return sales

    @staticmethod
    def resolve_net_cashflow(self, info, product_type, start_time, end_time):
        net_cashflow = (
            cdb.session.query(func.sum(TicketLaiu8CK.ticket_price))
            .filter(
                and_(
                    TicketLaiu8CK.create_time >= start_time,
                    TicketLaiu8CK.create_time <= end_time,
                    TicketLaiu8CK.product_type.in_(product_type),
                    TicketLaiu8CK.pay_id.isnot(None),
                )
            )
            .scalar()
        )
        return net_cashflow


class Query(ObjectType):
    grow_card = types.Field(GrowCardType)

    @staticmethod
    def resolve_grow_card(self, info):
        return GrowCardType
