from myapi.extensions import db
from myapi.struct.models import Tie_User_Role, Tie_User_PermitCode


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    value = db.Column(db.String(80))

    user = db.relationship(
        "User", secondary=Tie_User_Role, back_populates="role", lazy="bulk"
    )


class PermitCode(db.Model):
    __tablename__ = "permit_code"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    value = db.Column(db.String(80))

    user = db.relationship(
        "User",
        secondary=Tie_User_PermitCode,
        back_populates="permit_code",
        lazy="dynamic",
    )
