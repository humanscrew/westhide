from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity

from myapi.struct.schemas import RouteClosureTableSchema, RouteSchema, RouteTreeSchema
from myapi.struct.models import Route, RouteClosureTable, RouteTree, User
from myapi.utils import ClosureTable

defaultRoutes = [
    {
        "name": "Dashboard",
        "children": [
            {"name": "DashboardAnalysis"},
            {"name": "DashboardWorkbench"},
        ],
    },
    {
        "name": "System",
        "children": [
            {"name": "AccountManagement"},
            {"name": "RoleManagement"},
            {"name": "MenuManagement"},
        ],
    },
    {
        "name": "TicketManagement",
        "children": [
            {
                "name": "Laiu8TicketSystem",
                "children": [
                    {"name": "ClientManagement"},
                    {"name": "TicketSalesDetail"},
                    {"name": "Ticket2Finance"},
                ],
            },
        ],
    },
    {
        "name": "Voucher",
        "children": [
            {"name": "BookkeepingTemplate"},
            {"name": "VoucherGenerate"},
        ],
    },
]


class RouteResource(Resource):
    def get(self):
        pass


class RouteListResource(Resource):
    @staticmethod
    def get():
        user_id = get_jwt_identity()

        # ClosureTable(
        #     RouteTree, Route, RouteClosureTable, RouteSchema, RouteClosureTableSchema
        # ).create_tree(defaultRoutes)

        route_tree_ids = (
            User.query.get(user_id).route_tree.with_entities(RouteTree.id).all()
        )
        route_tree_schema = RouteTreeSchema(many=True)
        route_tree_ids = route_tree_schema.dump(route_tree_ids)
        route_tree_id_list = [item.get("id") for item in route_tree_ids]

        route_schema = RouteSchema(many=True)
        routes = User.query.get(user_id).route
        routes = route_schema.dump(routes)

        route_tree_list = ClosureTable(
            RouteTree, Route, RouteClosureTable, RouteSchema, RouteClosureTableSchema
        ).get_tree_list(routes, route_tree_id_list)

        for item in route_tree_list:
            item["path"] = "/" + item["path"]

        return {"result": route_tree_list}

    @staticmethod
    def post():
        routes = request.json.get("routes")
        ClosureTable(
            RouteTree, Route, RouteClosureTable, RouteSchema, RouteClosureTableSchema
        ).create_tree(routes)

        return {"message": "路由树创建成功"}, 201
