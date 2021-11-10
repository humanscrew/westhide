from myapi.extensions import ma, db
from myapi.models import SmsAliyun, SmsAliyunDetail
from marshmallow import INCLUDE


class SmsAliyunDetailSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = SmsAliyunDetail
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)
        unknown = INCLUDE


class SmsAliyunSchema(ma.SQLAlchemyAutoSchema):

    sms_aliyun_detail = ma.Nested(SmsAliyunDetailSchema, data_key="details")

    class Meta:
        model = SmsAliyun
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)
        include_fk = True
        unknown = INCLUDE
