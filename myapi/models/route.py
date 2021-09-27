from myapi.extensions import db

from myapi.models import Map_User_Route


class Route(db.Model):
    __tablename__ = "route"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(80))
    name = db.Column(db.String(80), unique=True)
    alias = db.Column(db.String(80))
    component = db.Column(db.String(255))
    redirect = db.Column(db.String(255))
    before_enter = db.Column(db.String(255))
    props = db.Column(db.String(255))
    route_meta_id = db.Column(db.Integer, db.ForeignKey("route_meta.id"))

    route_meta = db.relationship("RouteMeta", lazy="joined")

    user = db.relationship(
        "User",
        secondary=Map_User_Route,
        back_populates="route",
        lazy="dynamic"
    )


class RouteMeta(db.Model):
    __tablename__ = "route_meta"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    ignore_auth = db.Column(db.Boolean)
    roles = db.Column(db.String(80))
    ignore_keep_alive = db.Column(db.Boolean)
    affix = db.Column(db.Boolean)
    icon = db.Column(db.String(80))
    frame_src = db.Column(db.String(255))
    transition_name = db.Column(db.String(80))
    hide_breadcrumb = db.Column(db.Boolean)
    carry_param = db.Column(db.Boolean)
    hide_children_in_menu = db.Column(db.Boolean)
    current_active_menu = db.Column(db.String(255))
    hide_tab = db.Column(db.Boolean)
    order_no = db.Column(db.Integer)
    ignore_route = db.Column(db.Boolean)
    hide_path_for_children = db.Column(db.Boolean)


class RouteClosureTable(db.Model):
    __tablename__ = "route_closure_table"
    id = db.Column("id", db.Integer, primary_key=True)
    ancestor_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    descendant_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    depth = db.Column(db.Integer, nullable=False)

    ancestor_route = db.relationship("Route", foreign_keys=[ancestor_id])
    descendant_route = db.relationship("Route", foreign_keys=[descendant_id])
