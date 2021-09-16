from myapi.extensions import db
from myapi.models.user import Map_User_CompanyGroup, Map_User_SubsidiaryCompany

from datetime import datetime


class CompanyGroup(db.Model):
    __tablename__ = "company_group"
    id = db.Column(db.Integer, primary_key=True)
    financial_code = db.Column(db.String(20))
    name = db.Column(db.String(80))

    user = db.relationship(
        "User",
        secondary=Map_User_CompanyGroup,
        back_populates="company_group",
        lazy="dynamic"
    )


class SubsidiaryCompany(db.Model):
    __tablename__ = "subsidiary_company"
    id = db.Column(db.Integer, primary_key=True)
    uniform_social_credit_code = db.Column(db.String(20))
    financial_code = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(80))

    user = db.relationship(
        "User",
        secondary=Map_User_SubsidiaryCompany,
        back_populates="subsidiary_company",
        lazy="dynamic"
    )


class CooperateCompany(db.Model):
    __tablename__ = "cooperate_company"
    id = db.Column(db.Integer, primary_key=True)
    uniform_social_credit_code = db.Column(db.String(20))
    financial_code = db.Column(db.String(10))
    name = db.Column(db.String(80), nullable=False)
    alias = db.Column(db.String(80))
    create_time = db.Column(db.DATETIME, default=datetime.now)
    create_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    update_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)
    confirm_time = db.Column(db.DATETIME)
    confirm_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    status = db.Column(
        db.String(2),
        server_default="1",
        comment="1=on save;2=submitted;3=verified;4=to be modified;5=modified;6=abandon;"
    )

    create_user = db.relationship("User", foreign_keys=[create_user_id])
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
    begin_time = db.Column(db.DATETIME, default=datetime.now)
    end_time = db.Column(db.DATETIME)


class Map_Cooperate_Company(db.Model):
    __tablename__ = "map_cooperate_company"
    id = db.Column("id", db.Integer, primary_key=True)
    subsidiary_company_id = db.Column(db.Integer, db.ForeignKey("subsidiary_company.id"))
    cooperate_company_id = db.Column(db.Integer, db.ForeignKey("cooperate_company.id"))
    cooperate_type_id = db.Column(db.Integer, db.ForeignKey("cooperate_type.id"))

    subsidiary_company = db.relationship(
        "SubsidiaryCompany",
        foreign_keys=[subsidiary_company_id]
    )
    cooperate_company = db.relationship(
        "CooperateCompany",
        foreign_keys=[cooperate_company_id]
    )
    cooperate_type = db.relationship(
        "CooperateType",
        foreign_keys=[cooperate_type_id]
    )