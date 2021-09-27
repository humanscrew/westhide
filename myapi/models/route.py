from myapi.extensions import db


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
