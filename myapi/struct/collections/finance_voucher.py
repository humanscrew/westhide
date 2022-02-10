from myapi.extensions import mdb
from myapi.struct.collections import onupdate, BookkeepingTemplate


@onupdate.apply
class AuxiliaryAccountEmbed(mdb.EmbeddedDocument):
    code = mdb.StringField()
    name = mdb.StringField()
    value = mdb.StringField()


@onupdate.apply
class FinanceAccountEmbed(mdb.EmbeddedDocument):
    code = mdb.StringField()
    name = mdb.StringField()
    direction = mdb.StringField(max_length=1)
    auxiliaryAccounts = mdb.EmbeddedDocumentListField(
        AuxiliaryAccountEmbed, default=[AuxiliaryAccountEmbed()]
    )


@onupdate.apply
class FinanceVoucher(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField()
    bookkeepingTemplate = mdb.LazyReferenceField(BookkeepingTemplate)

    companyCode = mdb.StringField()
    bookkeepingDate = mdb.DateTimeField()
    businessDate = mdb.DateTimeField()
    period = mdb.StringField()
    type = mdb.StringField()
    voucherId = mdb.StringField()
    entryNo = mdb.StringField()
    abstract = mdb.StringField()
    currencyType = mdb.StringField(default="BB01")
    currencyRate = mdb.DecimalField(default=1)
    currencyAmount = mdb.DecimalField()
    direction = mdb.StringField(max_length=1)
    count = mdb.IntField()
    unitPrice = mdb.DecimalField()

    debitFinanceAccount = mdb.EmbeddedDocumentField(
        FinanceAccountEmbed, default=FinanceAccountEmbed()
    )
    debitAmount = mdb.DecimalField()

    creditFinanceAccount = mdb.EmbeddedDocumentField(
        FinanceAccountEmbed, default=FinanceAccountEmbed()
    )
    creditAmount = mdb.DecimalField()

    lister = mdb.StringField()
    auditor = mdb.StringField()
    confirmor = mdb.StringField()
    attachCount = mdb.IntField()
    isConfirm = mdb.BooleanField()
    machineModule = mdb.StringField()
    isDeleted = mdb.BooleanField(default=False)
    voucherNo = mdb.StringField()
    unit = mdb.StringField()
    referenceInformation = mdb.StringField()
    isCashflow = mdb.StringField()
    cashflowTag = mdb.StringField()
    businessNo = mdb.StringField()
    payment = mdb.StringField()
    payNo = mdb.StringField()
    dueDate = mdb.DateTimeField()
