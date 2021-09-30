from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from myapi.api.schemas import RouteClosureTableSchema, RouteSchema, RouteTreeSchema
from myapi.models import Route, RouteClosureTable, RouteTree, User
from myapi.utils import ClosureTable

defaultRoutes = [
    {
        "name": "Dashboard",
        "children": [
            {"name": "Analysis"},
            {"name": "Workbench"},
        ]
    },
    {
        "name": "System",
        "children": [
            {"name": "AccountManagement"},
            {"name": "RoleManagement"},
            {"name": "MenuManagement"},
        ]
    },
]


class RouteResource(Resource):

    def get(self):
        user_id = get_jwt_identity()

        routeTreeIds = User.query.get(user_id).route_tree.with_entities(RouteTree.id).all()
        routeTreeSchema = RouteTreeSchema(many=True)
        routeTreeIds = routeTreeSchema.dump(routeTreeIds)
        routeTreeIdList = [item.get("id") for item in routeTreeIds]

        routeSchema = RouteSchema(many=True)
        routes = User.query.get(user_id).route
        routes = routeSchema.dump(routes)

        routeTreeList = ClosureTable(
            RouteTree, Route, RouteClosureTable, RouteSchema, RouteClosureTableSchema
        ).getTreeList(routes, routeTreeIdList)

        for item in routeTreeList:
            item["path"] = "/" + item["path"]

        return {"routesList": routeTreeList}


class CreateRouteResource(Resource):

    def post(self):
        if not request.is_json:
            return {"message": "Missing JSON in request"}, 405
        routes = request.json.get("routes")
        ClosureTable(
            RouteTree, Route, RouteClosureTable, RouteSchema, RouteClosureTableSchema
        ).createTree(routes)
        return {"message": "路由树创建成功"}, 201
