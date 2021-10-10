from myapi.extensions import db


class FinanceAccount(db.Model):
    __tablename__ = "finance_account"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    caption = db.Column(db.String(80))
    direction = db.Column(db.String(1), comment="1=debit;0=credit")
    auxiliary_group_code = db.Column(db.String(80), db.ForeignKey("auxiliary_group.code"))

    auxiliary_group = db.relationship("AuxiliaryGroup", back_populates="finance_account")


class FinanceAccountTree(db.Model):
    __tablename__ = "finance_account_tree"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))


class FinanceAccountClosureTable(db.Model):
    __tablename__ = "finance_account_closure_table"
    id = db.Column("id", db.Integer, primary_key=True)
    tree_id = db.Column(db.Integer, db.ForeignKey("finance_account_tree.id"), nullable=False)
    ancestor_id = db.Column(db.Integer, db.ForeignKey('finance_account.id'), nullable=False)
    descendant_id = db.Column(db.Integer, db.ForeignKey('finance_account.id'), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    depth = db.Column(db.Integer, nullable=False)

    ancestor = db.relationship("FinanceAccount", foreign_keys=[ancestor_id])
    descendant = db.relationship("FinanceAccount", foreign_keys=[descendant_id])
    tree = db.relationship("FinanceAccountTree", foreign_keys=[tree_id])


Map_AuxiliaryGroup_AuxiliaryAccount = db.Table(
    "map_auxiliary_group2auxiliary_account",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("auxiliary_group_id", db.Integer, db.ForeignKey('auxiliary_group.id')),
    db.Column("auxiliary_account_id", db.Integer, db.ForeignKey('auxiliary_account.id'))
)


class AuxiliaryGroup(db.Model):
    __tablename__ = "auxiliary_group"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)

    finance_account = db.relationship("FinanceAccount", back_populates="auxiliary_group")

    auxiliary_account = db.relationship(
        "AuxiliaryAccount",
        secondary=Map_AuxiliaryGroup_AuxiliaryAccount,
        back_populates="auxiliary_group",
        lazy="dynamic"
    )


class AuxiliaryAccount(db.Model):
    __tablename__ = "auxiliary_account"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    title = db.Column(db.String(80), nullable=False)
    detail_table_name = db.Column(db.String(80))

    auxiliary_group = db.relationship(
        "AuxiliaryGroup",
        secondary=Map_AuxiliaryGroup_AuxiliaryAccount,
        back_populates="auxiliary_account",
        lazy="dynamic"
    )


class PaymentType(db.Model):
    __tablename__ = "payment_type"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    type = db.Column(db.String(80))


class TicketSeller(db.Model):
    __tablename__ = "ticket_seller"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80))


class ShipLine(db.Model):
    __tablename__ = "ship_line"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80))


class Ship(db.Model):
    __tablename__ = "ship"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80))


class BankAccount(db.Model):
    __tablename__ = "bank_account"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    account = db.Column(db.String(80), nullable=False, unique=True)
    account_name = db.Column(db.String(80))
    bank_name = db.Column(db.String(80))
    bank_branch_name = db.Column(db.String(80))
    bank_address = db.Column(db.String(80))
    create_date = db.Column(db.DATETIME)
    cancel_date = db.Column(db.DATETIME)


class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80))


class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80))


class BookkeepingTemplate(db.Model):
    __tablename__ = "bookkeeping_template"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80))
    company_code = db.Column(db.String(80))
    bookkeeping_date = db.Column(db.Date)
    business_date = db.Column(db.Date)
    period = db.Column(db.String(2))
    type = db.Column(db.String(10))
    voucher_id = db.Column(db.String(80))
    entry_no = db.Column(db.String(10))
    abstract = db.Column(db.String(80))
    currency_type = db.Column(db.String(10), default="BB01")
    currency_rate = db.Column(db.Float, default=1)
    direction = db.Column(db.String(1), comment="1=debit;0=credit")
    amount = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float, default=0)

    debit_finance_account_code = db.Column(db.String(80), db.ForeignKey("finance_account.code"))
    debit_amount = db.Column(db.Float)

    credit_finance_account_code = db.Column(db.String(80), db.ForeignKey("finance_account.code"))
    credit_amount = db.Column(db.Float)

    lister = db.Column(db.String(10))
    auditer = db.Column(db.String(10))
    confirmor = db.Column(db.String(10))
    attach_count = db.Column(db.Integer)
    is_confirm = db.Column(db.Boolean)
    machine_module = db.Column(db.String(80))
    is_deleted = db.Column(db.Boolean, default=False)
    voucher_no = db.Column(db.String(80))
    unit = db.Column(db.String(10))
    reference_information = db.Column(db.String(80))
    is_cashflow = db.Column(db.Boolean)
    cashflow_tag = db.Column(db.String(10))
    business_no = db.Column(db.String(80))
    payment = db.Column(db.String(10))
    pay_no = db.Column(db.String(80))
    due_date = db.Column(db.Date)

    debit_finance_account = db.relationship(
        "FinanceAccount",
        foreign_keys=[debit_finance_account_code]
    )
    credit_finance_account = db.relationship(
        "FinanceAccount",
        foreign_keys=[credit_finance_account_code]
    )
