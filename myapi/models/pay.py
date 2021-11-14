from myapi.extensions import db

from datetime import datetime


class TenPay(db.Model):
    __tablename__ = "tenpay_bill"
    id = db.Column(db.Integer, primary_key=True)
    trade_time = db.Column(db.DATETIME, index=True, comment='交易时间')
    appid = db.Column(db.String(80), comment='公众账号ID')
    mchid = db.Column(db.String(80), comment='商户号')
    special_mchid = db.Column(db.String(80), comment='特约商户号')
    device_id = db.Column(db.String(80), comment='设备号')
    transaction_id = db.Column(db.String(80), index=True, comment='微信订单号')
    out_trade_no = db.Column(db.String(80), index=True, comment='商户订单号')
    openid = db.Column(db.String(80), comment='用户标识')
    trade_type = db.Column(db.String(10), comment='交易类型')
    trade_state = db.Column(db.String(10), comment='交易状态')
    bank_type = db.Column(db.String(80), comment='付款银行')
    currency = db.Column(db.String(10), comment='货币种类')
    settlement_total = db.Column(db.DECIMAL(10, 3), index=True, comment='应结订单金额')
    discount_amount = db.Column(db.DECIMAL(10, 3), index=True, comment='代金券金额')
    refund_id = db.Column(db.String(80), index=True, comment='微信退款单号')
    out_refund_no = db.Column(db.String(80), comment='商户退款单号')
    refund_amount = db.Column(db.DECIMAL(10, 3), index=True, comment='退款金额')
    promotion_refund_amount = db.Column(db.DECIMAL(10, 3), index=True, comment='充值券退款金额')
    refund_type = db.Column(db.String(10), comment='退款类型')
    refund_status = db.Column(db.String(10), comment='退款状态')
    goods_name = db.Column(db.String(80), comment='商品名称')
    merchant_data_package = db.Column(db.String(80), comment='商户数据包')
    transaction_fee = db.Column(db.DECIMAL(10, 5), index=True, comment='手续费')
    transaction_rate = db.Column(db.String(80), comment='费率')
    bill_amount = db.Column(db.DECIMAL(10, 3), index=True, comment='订单金额')
    requested_refund_amount = db.Column(db.DECIMAL(10, 3), index=True, comment='申请退款金额')
    rate_remark = db.Column(db.String(80), comment='费率备注')
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)
