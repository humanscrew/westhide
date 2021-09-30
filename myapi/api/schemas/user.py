from myapi.api.schemas import RoleSchema
from myapi.models import User
from myapi.extensions import ma, db


class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    role = ma.Nested(RoleSchema, many=True, data_key="roles")

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password", "id")
        # include_fk = False
        # include_relationships = True
        # unknown = ma.INCLUDE
        # transient = True
