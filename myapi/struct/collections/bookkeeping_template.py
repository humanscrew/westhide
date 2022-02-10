from myapi.extensions import mdb
from myapi.struct.collections import onupdate


@onupdate.apply
class AuxiliaryAccount(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField(required=True)
    items = mdb.ListField(mdb.GenericLazyReferenceField())


@onupdate.apply
class AuxiliaryGroup(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField(required=True)
    auxiliaryAccounts = mdb.ListField(
        mdb.ReferenceField("AuxiliaryAccount", reverse_delete_rule=mdb.DENY)
    )


@onupdate.apply
class FinanceAccount(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField(required=True)
    direction = mdb.StringField(max_length=1)
    auxiliaryGroup = mdb.ReferenceField("AuxiliaryGroup", reverse_delete_rule=mdb.DENY)


@onupdate.apply
class PaymentType(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField(required=True)


@onupdate.apply
class ShipLine(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField(required=True)


@onupdate.apply
class Ship(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField(required=True)


@onupdate.apply
class BankAccount(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    account = mdb.StringField(required=True, unique=True)
    accountName = mdb.StringField(required=True)
    bankName = mdb.StringField(required=True)
    bankBranchName = mdb.StringField()
    bankBranchAddress = mdb.StringField()
    createDate = mdb.DateTimeField()
    cancelDate = mdb.DateTimeField()


@onupdate.apply
class Employee(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField(required=True)


@onupdate.apply
class Department(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField(required=True)


@onupdate.apply
class FinanceClient(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField(required=True)


@onupdate.apply
class BookkeepingTemplate(mdb.Document):
    code = mdb.StringField(required=True, unique=True)
    name = mdb.StringField(required=True)

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

    debitFinanceAccount = mdb.ReferenceField(
        "FinanceAccount", reverse_delete_rule=mdb.DENY, required=True
    )
    debitAmount = mdb.DecimalField()

    creditFinanceAccount = mdb.ReferenceField(
        "FinanceAccount", reverse_delete_rule=mdb.DENY, required=True
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
