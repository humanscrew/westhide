from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from myapi.api.schemas import CompanyGroupSchema
from myapi.models import User, CompanyGroup


class CompanyGroupResource(Resource):

    def get(self):
        companyGroupSchema = CompanyGroupSchema(many=True)
        user_id = get_jwt_identity()
        companyGroups = User.query.get_or_404(user_id).company_group.with_entities(
            CompanyGroup.name, CompanyGroup.icon, CompanyGroup.color, CompanyGroup.desc, CompanyGroup.location
        )
        return {"companyGroup": companyGroupSchema.dump(companyGroups)}
