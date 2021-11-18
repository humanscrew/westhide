from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from myapi.api.schemas import PermitCodeSchema
from myapi.models import User


class PermitCodeResource(Resource):

    @staticmethod
    def get():
        permit_code_schema = PermitCodeSchema(many=True)
        user_id = get_jwt_identity()
        permit_codes = User.query.get_or_404(user_id).permit_code

        return {"permitCode": permit_code_schema.dump(permit_codes)}
