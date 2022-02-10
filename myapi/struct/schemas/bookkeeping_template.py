from marshmallow_mongoengine import ModelSchema

from marshmallow.fields import Nested

from myapi.struct.collections import (
    AuxiliaryAccount,
    AuxiliaryGroup,
    FinanceAccount,
    BookkeepingTemplate,
)


class AuxiliaryAccountSchema(ModelSchema):
    class Meta:
        model = AuxiliaryAccount
        model_skip_values = ()


class AuxiliaryGroupSchema(ModelSchema):
    auxiliaryAccounts = Nested(AuxiliaryAccountSchema, many=True)

    class Meta:
        model = AuxiliaryGroup
        model_skip_values = ()
        exclude = ("auxiliaryAccounts",)


class FinanceAccountSchema(ModelSchema):
    auxiliaryGroup = Nested(AuxiliaryGroupSchema)

    class Meta:
        model = FinanceAccount
        model_skip_values = ()


class BookkeepingTemplateSchema(ModelSchema):
    debitFinanceAccount = Nested(FinanceAccountSchema)
    creditFinanceAccount = Nested(FinanceAccountSchema)

    class Meta:
        model = BookkeepingTemplate
        model_skip_values = ()
