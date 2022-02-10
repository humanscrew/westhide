from myapi.extensions import db
from myapi.struct.models import Tie_User_CompanyGroup, Tie_User_SubsidiaryCompany
from sqlalchemy import func

Tie_CompanyGroup_SubsidiaryCompany = db.Table(
    "tie_company_group_2_subsidiary_company",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("company_group_id", db.Integer, db.ForeignKey("company_group.id")),
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


class CompanyGroup(db.Model):
    __tablename__ = "company_group"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    name = db.Column(db.String(80))
    desc = db.Column(db.String(80))
    icon = db.Column(db.String(80))
    color = db.Column(db.String(80))
    address = db.Column(db.String(80))
    location = db.Column(db.String(80))

    user = db.relationship(
        "User",
        secondary=Tie_User_CompanyGroup,
        back_populates="company_group",
        lazy="dynamic",
    )

    subsidiary_company = db.relationship(
        "SubsidiaryCompany",
        secondary=Tie_CompanyGroup_SubsidiaryCompany,
        back_populates="company_group",
        lazy="dynamic",
    )


class SubsidiaryCompany(db.Model):
    __tablename__ = "subsidiary_company"
    id = db.Column(db.Integer, primary_key=True)
    uniform_social_credit_code = db.Column(db.String(20))
    code = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(80))

    user = db.relationship(
        "User",
        secondary=Tie_User_SubsidiaryCompany,
        back_populates="subsidiary_company",
        lazy="dynamic",
    )

    company_group = db.relationship(
        "CompanyGroup",
        secondary=Tie_CompanyGroup_SubsidiaryCompany,
        back_populates="subsidiary_company",
        lazy="dynamic",
    )


class CooperateCompany(db.Model):
    __tablename__ = "cooperate_company"
    id = db.Column(db.Integer, primary_key=True)
    uniform_social_credit_code = db.Column(db.String(20))
    code = db.Column(db.String(10))
    name = db.Column(db.String(80), nullable=False)
    alias = db.Column(db.String(80))
    create_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    update_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    confirm_time = db.Column(db.TIMESTAMP)
    confirm_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    status = db.Column(
        db.String(2),
        server_default="1",
        comment="1=on save;2=submitted;3=verified;4=to be modified;5=modified;6=abandon;",
    )

    create_user = db.relationship("User", foreign_keys=[create_user_id])
    update_user = db.relationship("User", foreign_keys=[update_user_id])
    confirm_user = db.relationship("User", foreign_keys=[confirm_user_id])


class CooperateType(db.Model):
    __tablename__ = "cooperate_type"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))


class CompanyNameHistory(db.Model):
    __tablename__ = "company_name_history"
    id = db.Column(db.Integer, primary_key=True)
    uniform_social_credit_code = db.Column(db.String(20))
    name = db.Column(db.String(80))
    begin_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)


class Map_Cooperate_Company(db.Model):
    __tablename__ = "map_cooperate_company"
    id = db.Column("id", db.Integer, primary_key=True)
    subsidiary_company_id = db.Column(
        db.Integer, db.ForeignKey("subsidiary_company.id")
    )
    cooperate_company_id = db.Column(db.Integer, db.ForeignKey("cooperate_company.id"))
    cooperate_type_id = db.Column(db.Integer, db.ForeignKey("cooperate_type.id"))

    subsidiary_company = db.relationship(
        "SubsidiaryCompany", foreign_keys=[subsidiary_company_id]
    )
    cooperate_company = db.relationship(
        "CooperateCompany", foreign_keys=[cooperate_company_id]
    )
    cooperate_type = db.relationship("CooperateType", foreign_keys=[cooperate_type_id])
