from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from myapi.api.schemas import CompanyGroupSchema
from myapi.models import User, CompanyGroup


class CompanyGroupResource(Resource):

    @staticmethod
    def get():
        company_group_schema = CompanyGroupSchema(many=True)
        user_id = get_jwt_identity()
        company_groups = User.query.get_or_404(user_id).company_group.with_entities(
            CompanyGroup.name, CompanyGroup.icon, CompanyGroup.color, CompanyGroup.desc, CompanyGroup.location
        )

        return {"companyGroups": company_group_schema.dump(company_groups)}
