from myapi.extensions import db


class RSAModel(db.Model):
    __tablename__ = "utils_rsa"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True
    )
    public_key = db.Column(db.Text, nullable=False)
    private_key = db.Column(db.Text, nullable=False)

    user = db.relationship(
        "User",
        backref=db.backref("utils_rsa", uselist=False),
        uselist=False,
        lazy="joined",
    )


class DefaultRSAModel(db.Model):
    __tablename__ = "utils_default_rsa"
    id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.Text, nullable=False)
    private_key = db.Column(db.Text, nullable=False)
