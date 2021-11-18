from myapi.extensions import db
from myapi.models import Map_User_Role, Map_User_PermitCode

from datetime import datetime


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    value = db.Column(db.String(80))
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)

    user = db.relationship(
        "User",
        secondary=Map_User_Role,
        back_populates="role",
        lazy="dynamic"
    )


class PermitCode(db.Model):
    __tablename__ = "permit_code"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    value = db.Column(db.String(80))
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)

    user = db.relationship(
        "User",
        secondary=Map_User_PermitCode,
        back_populates="permit_code",
        lazy="dynamic"
    )
