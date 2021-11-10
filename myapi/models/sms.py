from myapi.extensions import db

from datetime import datetime


class SmsAliyun(db.Model):
    __tablename__ = 'sms_aliyun'
    id = db.Column(db.Integer, primary_key=True)
    biz_id = db.Column(db.String(80),nullable=False, unique=True)
    phone_numbers = db.Column(db.Text, nullable=False)
    sign_name = db.Column(db.String(80), nullable=False)
    template_code = db.Column(db.String(80), nullable=False)
    template_param = db.Column(db.Text, nullable=False)
    send_date = db.Column(db.String(10), nullable=False)

    request_id = db.Column(db.String(80))
    code = db.Column(db.String(80))
    message = db.Column(db.String(80))
    total_count = db.Column(db.String(10))
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)

    sms_aliyun_detail = db.relationship("SmsAliyunDetail", back_populates="sms_aliyun")


class SmsAliyunDetail(db.Model):
    __tablename__ = "sms_aliyun_detail"
    id = db.Column(db.Integer, primary_key=True)
    biz_id = db.Column(db.String(80),db.ForeignKey("sms_aliyun.biz_id"))
    request_id = db.Column(db.String(80))
    err_code = db.Column(db.String(80))
    template_code = db.Column(db.String(80))
    out_id = db.Column(db.String(80))
    receive_date = db.Column(db.DateTime)
    send_date = db.Column(db.DateTime)
    phone_num = db.Column(db.String(20))
    context = db.Column(db.Text)
    send_status = db.Column(db.String(10), comment="1=等待回执,2=发送失败,3=发送成功")
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)

    sms_aliyun = db.relationship("SmsAliyun", back_populates="sms_aliyun_detail")
