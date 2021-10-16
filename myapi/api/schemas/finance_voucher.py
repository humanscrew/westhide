from marshmallow_mongoengine import ModelSchema

from marshmallow.fields import Nested

from myapi.collections import AuxiliaryAccountEmbed, FinanceAccountEmbed, FinanceVoucher


class AuxiliaryAccountEmbedSchema(ModelSchema):

    class Meta:
        model = AuxiliaryAccountEmbed
        model_skip_values = ()


class FinanceAccountEmbedSchema(ModelSchema):

    auxiliaryAccounts = Nested(AuxiliaryAccountEmbedSchema, many=True)

    class Meta:
        model = FinanceAccountEmbed
        model_skip_values = ()


class FinanceVoucherSchema(ModelSchema):

    debitFinanceAccount = Nested(FinanceAccountEmbedSchema)
    creditFinanceAccount = Nested(FinanceAccountEmbedSchema)

    class Meta:
        model = FinanceVoucher
        model_skip_values = ()
