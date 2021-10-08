"""empty message

Revision ID: 8be873b397f4
Revises: 483588f52d5c
Create Date: 2021-10-02 03:45:13.393346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8be873b397f4'
down_revision = '483588f52d5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket_laiu8',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_lock', sa.Boolean(), nullable=True, comment='状态锁定'),
    sa.Column('order_id', sa.String(length=80), nullable=True, comment='订单ID'),
    sa.Column('order_no', sa.String(length=80), nullable=True, comment='订单号'),
    sa.Column('channel_name', sa.String(length=80), nullable=True, comment='渠道=来游吧/北海窗口/涠洲窗口/票务室/内部订票/驻岛订票...'),
    sa.Column('create_time', sa.DATETIME(), nullable=True, comment='下单时间'),
    sa.Column('user_id', sa.String(length=80), nullable=True, comment='用户ID'),
    sa.Column('user_type', sa.String(length=80), nullable=True, comment='用户类型=OTA/VIP/窗口/散客'),
    sa.Column('user_name', sa.String(length=80), nullable=True, comment='用户名称/下单人名称'),
    sa.Column('mobile', sa.String(length=80), nullable=True, comment='下单人手机号'),
    sa.Column('ticket_no', sa.String(length=80), nullable=True, comment='票号'),
    sa.Column('ticket_type_name', sa.String(length=80), nullable=True, comment='票型'),
    sa.Column('product_type', sa.String(length=80), nullable=True, comment='产品类型'),
    sa.Column('ticket_status', sa.String(length=80), nullable=True, comment='船票状态=已取消/出票成功/一检/二检/改签废票/已退款/已改签/已升舱...'),
    sa.Column('departure_datetime', sa.DATETIME(), nullable=True, comment='航班时间'),
    sa.Column('linename', sa.String(length=80), nullable=True, comment='航线名称=北海-涠洲/涠洲-北海/北海-海口...'),
    sa.Column('ship_name', sa.String(length=80), nullable=True, comment='船舶名称'),
    sa.Column('cabin_name', sa.String(length=80), nullable=True, comment='船舱名称'),
    sa.Column('seat_memo', sa.String(length=80), nullable=True, comment='座位号'),
    sa.Column('passenger_name', sa.String(length=80), nullable=True, comment='乘客姓名'),
    sa.Column('passenger_id_no', sa.String(length=80), nullable=True, comment='乘客身份证号'),
    sa.Column('full_ticket_price', sa.Integer(), nullable=True, comment='原价'),
    sa.Column('discount_price', sa.Integer(), nullable=True, comment='票价折扣'),
    sa.Column('ticket_price', sa.Integer(), nullable=True, comment='实际票价=原价-票价折扣'),
    sa.Column('get_voucher', sa.Integer(), nullable=True, comment='产生的积分'),
    sa.Column('use_voucher', sa.Integer(), nullable=True, comment='使用的积分'),
    sa.Column('payment_time', sa.DATETIME(), nullable=True, comment='支付时间'),
    sa.Column('payment_method', sa.String(length=80), nullable=True, comment='支付方式=现金/POS机/微信/支付宝/来游吧OTA预存款/转账'),
    sa.Column('pay_id', sa.String(length=80), nullable=True, comment='支付ID=<微信订单号>/<支付宝业务流水号>'),
    sa.Column('real_price', sa.Integer(), nullable=True, comment='实际支付价格=实际票价-使用的积分=<微信订单金额>/<支付宝收入金额>'),
    sa.Column('change_type', sa.String(length=80), nullable=True, comment='票状态变更=已退款/已改签/已升舱...'),
    sa.Column('ticket_no_new', sa.String(length=80), nullable=True, comment='[链接表]状态变更产生新票的票号/未产生为NULL'),
    sa.Column('change_time', sa.DATETIME(), nullable=True, comment='操作时间'),
    sa.Column('ticket_change_channel_name', sa.String(length=80), nullable=True, comment='操作渠道=/'),
    sa.Column('change_user_name', sa.String(length=80), nullable=True, comment='状态变更操作人'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket_laiu8_refund',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticket_no', sa.String(length=80), nullable=True, comment='foreign_key=ticket_laiu8.ticket_no'),
    sa.Column('ticket_refund_method', sa.String(length=80), nullable=True, comment='退款方式=/'),
    sa.Column('ticket_refund_finish_time', sa.DATETIME(), nullable=True, comment='实际退款时间'),
    sa.Column('refund_id', sa.String(length=80), nullable=True, comment='退款ID=<微信商户退款单号>/<支付宝商户订单号>'),
    sa.Column('fee', sa.Integer(), nullable=True, comment='手续费'),
    sa.Column('refund_amount', sa.Integer(), nullable=True, comment='退款金额'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticket_laiu8_refund')
    op.drop_table('ticket_laiu8')
    # ### end Alembic commands ###