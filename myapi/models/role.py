from myapi.extensions import db
from myapi.models.user import Map_User_Role


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    value = db.Column(db.String(80))

    user = db.relationship(
        "User",
        secondary=Map_User_Role,
        back_populates="role",
        lazy="dynamic"
    )
