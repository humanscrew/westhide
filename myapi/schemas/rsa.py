from myapi.extensions import db, ma
from myapi.models import RSAModel, DefaultRSAModel


class RSASchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RSAModel
        sqla_session = db.session
        load_instance = True
        include_fk = True
        exclude = ("id",)


class DefaultRSASchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DefaultRSAModel
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)
