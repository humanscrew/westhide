from sqlalchemy.ext.hybrid import hybrid_property

from myapi.extensions import db, pwd_context

from datetime import datetime

Map_User_CompanyGroup = db.Table(
    "map_user2company_group",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
    db.Column("company_group_id", db.Integer, db.ForeignKey('company_group.id'))
)

Map_User_SubsidiaryCompany = db.Table(
    "map_user2subsidiary_company",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
    db.Column("subsidiary_company_id", db.Integer, db.ForeignKey('subsidiary_company.id'))
)

Map_User_Role = db.Table(
    "map_user2role",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
    db.Column("role_id", db.Integer, db.ForeignKey('role.id'))
)

Map_User_PermitCode = db.Table(
    "map_user2permit_code",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
    db.Column("permit_code_id", db.Integer, db.ForeignKey('permit_code.id'))
)


class User(db.Model):
    """Basic user model"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    mobile = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)
    real_name = db.Column(db.String(80))

    company_group = db.relationship(
        'CompanyGroup',
        secondary=Map_User_CompanyGroup,
        back_populates="user",
        lazy='dynamic'
    )
    subsidiary_company = db.relationship(
        'SubsidiaryCompany',
        secondary=Map_User_SubsidiaryCompany,
        back_populates="user",
        lazy='dynamic'
    )
    role = db.relationship(
        'Role',
        secondary=Map_User_Role,
        back_populates="user",
        lazy='dynamic'
    )
    permit_code = db.relationship(
        'PermitCode',
        secondary=Map_User_PermitCode,
        back_populates="user",
        lazy='dynamic'
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s>" % self.username
