from myapi.extensions import mdb


class AuxiliaryAccount(mdb.EmbeddedDocument):

    code = mdb.StringField(required=True, primary_key=True)
    name = mdb.StringField()
    referenceCollection = mdb.GenericReferenceField()


class AuxiliaryGroup(mdb.Document):

    code = mdb.StringField(required=True, primary_key=True)
    name = mdb.StringField()
    AuxiliaryAccounts = mdb.EmbeddedDocumentListField(AuxiliaryAccount)


class FinanceAccount(mdb.Document):

    code = mdb.StringField(required=True, primary_key=True)
    name = mdb.StringField()
    direction = mdb.StringField(max_length=1)
    auxiliaryGroup = mdb.ReferenceField('AuxiliaryGroup', reverse_delete_rule=mdb.DENY)


class Payment(mdb.Document):

    code = mdb.StringField(required=True, primary_key=True)
    name = mdb.StringField()


class ShipLine(mdb.Document):

    code = mdb.StringField(required=True, primary_key=True)
    name = mdb.StringField()


class Ship(mdb.Document):

    code = mdb.StringField(required=True, primary_key=True)
    name = mdb.StringField()


class BankAccount(mdb.Document):

    code = mdb.StringField(required=True, primary_key=True)
    account = mdb.StringField()
    accountName = mdb.StringField()
    bankName = mdb.StringField()
    bankBranchName = mdb.StringField()
    bankBranchAddress = mdb.StringField()
    createDate = mdb.DateTimeField()
    cancelDate = mdb.DateTimeField()


class Employee(mdb.Document):

    code = mdb.StringField(required=True, primary_key=True)
    name = mdb.StringField()


class Department(mdb.Document):

    code = mdb.StringField(required=True, primary_key=True)
    name = mdb.StringField()


class BookkeepingTemplate(mdb.Document):

    code = mdb.StringField(required=True, primary_key=True)
    name = mdb.StringField()

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

    debitFinanceAccount = mdb.ReferenceField('FinanceAccount', reverse_delete_rule=mdb.DENY)
    debitAmount = mdb.DecimalField()

    creditFinanceAccount = mdb.ReferenceField('FinanceAccount', reverse_delete_rule=mdb.DENY)
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

    meta = {'abstract': True, }


class FinanceVoucher(BookkeepingTemplate):

    code = mdb.StringField()
