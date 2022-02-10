from myapi.extensions import ma, db
from myapi.struct.models import CompanyGroup


class CompanyGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CompanyGroup
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)
