from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from myapi.api.schemas import PermitCodeSchema
from myapi.models import User


class PermitCodeResource(Resource):
    def get(self):
        permitCodeSchema = PermitCodeSchema(many=True)
        user_id = get_jwt_identity()
        permitCode = User.query.get_or_404(user_id).permit_code
        return {"permitCode": permitCodeSchema.dump(permitCode)}
