from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func

from myapi.extensions import db, pwd_context


Tie_User_CompanyGroup = db.Table(
    "tie_user_2_company_group",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("company_group_id", db.Integer, db.ForeignKey("company_group.id")),
    db.Column("created_at", db.TIMESTAMP, server_default=func.now()),
    db.Column(
        "updated_at",
        db.TIMESTAMP,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
)

Tie_User_SubsidiaryCompany = db.Table(
    "tie_user_2_subsidiary_company",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column(
        "subsidiary_company_id", db.Integer, db.ForeignKey("subsidiary_company.id")
    ),
    db.Column("created_at", db.TIMESTAMP, server_default=func.now()),
    db.Column(
        "updated_at",
        db.TIMESTAMP,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
)

Tie_User_Role = db.Table(
    "tie_user_2_role",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("created_at", db.TIMESTAMP, server_default=func.now()),
    db.Column(
        "updated_at",
        db.TIMESTAMP,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
)

Tie_User_PermitCode = db.Table(
    "tie_user_2_permit_code",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("permit_code_id", db.Integer, db.ForeignKey("permit_code.id")),
    db.Column("created_at", db.TIMESTAMP, server_default=func.now()),
    db.Column(
        "updated_at",
        db.TIMESTAMP,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
)

Tie_User_Route = db.Table(
    "tie_user_2_route",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("route_id", db.Integer, db.ForeignKey("route.id")),
    db.Column("created_at", db.TIMESTAMP, server_default=func.now()),
    db.Column(
        "updated_at",
        db.TIMESTAMP,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
)

Tie_User_Route_Tree = db.Table(
    "tie_user_2_route_tree",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("route_tree_id", db.Integer, db.ForeignKey("route_tree.id")),
    db.Column("created_at", db.TIMESTAMP, server_default=func.now()),
    db.Column(
        "updated_at",
        db.TIMESTAMP,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    nickname = db.Column(db.String(80))
    mobile = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True)
    _password = db.Column("password", db.String(255), nullable=False, index=True)
    active = db.Column(db.Boolean, default=True)
    real_name = db.Column(db.String(80))
    remark = db.Column(db.String(80))

    company_group = db.relationship(
        "CompanyGroup",
        secondary=Tie_User_CompanyGroup,
        back_populates="user",
        lazy="dynamic",
    )

    subsidiary_company = db.relationship(
        "SubsidiaryCompany",
        secondary=Tie_User_SubsidiaryCompany,
        back_populates="user",
        lazy="dynamic",
    )

    role = db.relationship(
        "Role", secondary=Tie_User_Role, back_populates="user", lazy="bulk"
    )

    permit_code = db.relationship(
        "PermitCode",
        secondary=Tie_User_PermitCode,
        back_populates="user",
        lazy="dynamic",
    )

    route = db.relationship(
        "Route", secondary=Tie_User_Route, back_populates="user", lazy="dynamic"
    )

    route_tree = db.relationship(
        "RouteTree",
        secondary=Tie_User_Route_Tree,
        back_populates="user",
        lazy="dynamic",
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s>" % self.username
