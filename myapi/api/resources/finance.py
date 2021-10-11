from flask_restful import Resource, request

from myapi.models import BookkeepingTemplate
from myapi.api.schemas import BookkeepingTemplateSchema

from myapi.utils import HandleQuery


class BookkeepingTemplateResource(Resource):

    def get(self):

        bookkeepingTemplateSchema = BookkeepingTemplateSchema(many=True)
        bookkeepingTemplate = HandleQuery(BookkeepingTemplate, bookkeepingTemplateSchema, request).deal()

        return bookkeepingTemplate.paginate()
