from myapi.models import CompanyGroup
from myapi.extensions import ma, db


class CompanyGroupSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = CompanyGroup
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)
