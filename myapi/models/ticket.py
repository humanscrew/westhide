from myapi.extensions import db

from datetime import datetime

from myapi.extensions import cdb
from sqlalchemy import Column, func
from clickhouse_sqlalchemy import types, engines


class TicketLaiu8(db.Model):
    __tablename__ = "ticket_laiu8"
    id = db.Column(db.Integer, primary_key=True, index=True)
    is_lock = db.Column(db.Boolean, index=True, comment="状态锁定")
    order_id = db.Column(db.String(80), index=True, comment="订单ID")
    order_no = db.Column(db.String(80), index=True, comment="订单号")
    channel_name = db.Column(
        db.String(80), index=True, comment="渠道=来游吧/北海窗口/涠洲窗口/票务室/内部订票/驻岛订票..."
    )
    create_time = db.Column(db.DATETIME, index=True, comment="下单时间")
    user_id = db.Column(db.String(80), index=True, comment="用户ID")
    user_type = db.Column(db.String(80), index=True, comment="用户类型=OTA/VIP/窗口/散客")
    user_name = db.Column(db.String(80), index=True, comment="用户名称/下单人名称")
    mobile = db.Column(db.String(80), index=True, comment="下单人手机号")
    ticket_no = db.Column(db.String(80), index=True, comment="票号")
    ticket_type_name = db.Column(db.String(80), index=True, comment="票型")
    product_type = db.Column(db.String(80), index=True, comment="产品类型")
    ticket_status = db.Column(
        db.String(80), index=True, comment="船票状态=已取消/出票成功/一检/二检/改签废票/已退款/已改签/已升舱..."
    )
    departure_datetime = db.Column(db.DATETIME, index=True, comment="航班时间")
    line_name = db.Column(
        db.String(80), index=True, comment="航线名称=北海-涠洲/涠洲-北海/北海-海口..."
    )
    ship_name = db.Column(db.String(80), index=True, comment="船舶名称")
    cabin_name = db.Column(db.String(80), index=True, comment="船舱名称")
    seat_memo = db.Column(db.String(80), index=True, comment="座位号")
    passenger_name = db.Column(db.String(80), index=True, comment="乘客姓名")
    passenger_id_no = db.Column(db.String(80), index=True, comment="乘客身份证号")
    full_ticket_price = db.Column(db.DECIMAL(10, 3), index=True, comment="原价")
    discount_price = db.Column(db.DECIMAL(10, 3), index=True, comment="票价折扣")
    ticket_price = db.Column(db.DECIMAL(10, 3), index=True, comment="实际票价=原价-票价折扣")
    get_voucher = db.Column(db.DECIMAL(10, 3), index=True, comment="产生的积分")
    use_voucher = db.Column(db.DECIMAL(10, 3), index=True, comment="使用的积分")
    payment_time = db.Column(db.DATETIME, index=True, comment="支付时间")
    payment_method = db.Column(
        db.String(80), index=True, comment="支付方式=现金/POS机/微信/支付宝/来游吧OTA预存款/转账"
    )
    pay_id = db.Column(db.String(80), index=True, comment="支付ID=<微信订单号>/<支付宝业务流水号>")
    real_price = db.Column(
        db.DECIMAL(10, 3), index=True, comment="实际支付价格=实际票价-使用的积分=<微信订单金额>/<支付宝收入金额>"
    )
    change_type = db.Column(db.String(80), index=True, comment="票状态变更=已退款/已改签/已升舱...")
    ticket_no_new = db.Column(
        db.String(80), index=True, comment="[链接表]状态变更产生新票的票号/未产生为NULL"
    )
    change_time = db.Column(db.DATETIME, index=True, comment="操作时间")
    ticket_change_channel_name = db.Column(db.String(80), index=True, comment="操作渠道=/")
    change_user_name = db.Column(db.String(80), index=True, comment="状态变更操作人")

    ticket_laiu8_refund = db.relationship(
        "TicketLaiu8Refund", back_populates="ticket_laiu8"
    )


class TicketLaiu8Refund(db.Model):
    __tablename__ = "ticket_laiu8_refund"
    id = db.Column(db.Integer, primary_key=True)
    ticket_laiu8_id = db.Column(db.Integer, db.ForeignKey("ticket_laiu8.id"))
    ticket_no = db.Column(db.String(80), index=True)
    ticket_refund_method = db.Column(db.String(80), index=True, comment="退款方式=/")
    ticket_refund_finish_time = db.Column(db.DATETIME, index=True, comment="实际退款时间")
    refund_id = db.Column(
        db.String(80), index=True, comment="退款ID=<微信商户退款单号>/<支付宝商户订单号>"
    )
    fee = db.Column(db.DECIMAL(10, 3), index=True, comment="手续费")
    refund_amount = db.Column(db.DECIMAL(10, 3), index=True, comment="退款金额")

    ticket_laiu8 = db.relationship("TicketLaiu8", back_populates="ticket_laiu8_refund")


class Laiu8Client(db.Model):
    __tablename__ = "ticket_laiu8_client"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(20))
    uniform_social_credit_code = db.Column(db.String(20))
    type = db.Column(db.String(20))
    name = db.Column(db.String(80))
    company_name = db.Column(db.String(80))
    mobile = db.Column(db.String(80))
    address = db.Column(db.String(80))
    cooperate_start_time = db.Column(db.DATETIME)
    cooperate_end_time = db.Column(db.DATETIME)
    manager = db.Column(db.String(80))
    sales = db.Column(db.DECIMAL(10, 3))
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)


class Ticket2Finance(db.Model):
    __tablename__ = "ticket2finance"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    date = db.Column(db.Date)
    payment_method = db.Column(
        db.String(80), comment="支付方式=现金/POS机/微信/支付宝/来游吧OTA预存款/转账"
    )
    user_type = db.Column(db.String(80), comment="用户类型=OTA/VIP/窗口/散客")
    user_name = db.Column(db.String(80), comment="用户名称/下单人名称")
    product_type = db.Column(db.String(80), comment="产品类型")
    ticket_price = db.Column(db.DECIMAL(10, 3), comment="实际票价=原价-票价折扣")
    get_voucher = db.Column(db.DECIMAL(10, 3), comment="产生的积分")
    use_voucher = db.Column(db.DECIMAL(10, 3), comment="使用的积分")
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)


class TicketLaiu8CK(cdb.Model):
    __tablename__ = "ticket_laiu8"
    id = Column(types.Int32, primary_key=True)
    is_lock = Column(types.Nullable(types.Int8))
    order_id = Column(types.String)
    order_no = Column(types.Nullable(types.String))
    channel_name = Column(types.Nullable(types.String))
    create_time = Column(types.DateTime)
    user_id = Column(types.Nullable(types.String))
    user_type = Column(types.Nullable(types.String))
    user_name = Column(types.Nullable(types.String))
    mobile = Column(types.Nullable(types.String))
    ticket_no = Column(types.Nullable(types.String))
    ticket_type_name = Column(types.Nullable(types.String))
    product_type = Column(types.Nullable(types.String))
    ticket_status = Column(types.Nullable(types.String))
    departure_datetime = Column(types.Nullable(types.DateTime))
    line_name = Column(types.Nullable(types.String))
    ship_name = Column(types.Nullable(types.String))
    cabin_name = Column(types.Nullable(types.String))
    seat_memo = Column(types.Nullable(types.String))
    passenger_name = Column(types.Nullable(types.String))
    passenger_id_no = Column(types.Nullable(types.String))
    full_ticket_price = Column(types.Nullable(types.Decimal(10, 3)))
    discount_price = Column(types.Nullable(types.Decimal(10, 3)))
    ticket_price = Column(types.Nullable(types.Decimal(10, 3)))
    get_voucher = Column(types.Nullable(types.Decimal(10, 3)))
    use_voucher = Column(types.Nullable(types.Decimal(10, 3)))
    payment_time = Column(types.Nullable(types.DateTime))
    payment_method = Column(types.Nullable(types.String))
    pay_id = Column(types.Nullable(types.String))
    real_price = Column(types.Nullable(types.Decimal(10, 3)))
    change_type = Column(types.Nullable(types.String))
    ticket_no_new = Column(types.Nullable(types.String))
    change_time = Column(types.Nullable(types.DateTime))
    ticket_change_channel_name = Column(types.Nullable(types.String))
    change_user_name = Column(types.Nullable(types.String))

    __table_args__ = (engines.MergeTree(partition_by=(func.toDate(create_time),), order_by=('id',)),)
