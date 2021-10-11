from myapi.models import AuxiliaryAccount, AuxiliaryGroup, FinanceAccount, BookkeepingTemplate

from myapi.extensions import ma, db


class AuxiliaryAccountSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = AuxiliaryAccount
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)


class AuxiliaryGroupSchema(ma.SQLAlchemyAutoSchema):

    auxiliary_account = ma.Nested(AuxiliaryAccountSchema, many=True)

    class Meta:
        model = AuxiliaryGroup
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)


class FinanceAccountSchema(ma.SQLAlchemyAutoSchema):

    auxiliary_group = ma.Nested(AuxiliaryGroupSchema)

    class Meta:
        model = FinanceAccount
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)


class BookkeepingTemplateSchema(ma.SQLAlchemyAutoSchema):

    debit_finance_account = ma.Nested(FinanceAccountSchema)
    credit_finance_account = ma.Nested(FinanceAccountSchema)

    class Meta:
        model = BookkeepingTemplate
        sqla_session = db.session
        load_instance = True
        exclude = ("id",)
