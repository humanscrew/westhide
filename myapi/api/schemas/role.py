from myapi.models import Role, PermitCode
from myapi.extensions import ma, db


class RoleSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Role
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)


class PermitCodeSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = PermitCode
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)
