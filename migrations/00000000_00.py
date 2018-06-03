import src.prod_database as prod_database_controller
from playhouse.postgres_ext import BinaryJSONField, DateTimeTZField
import peewee


class BaseModel(peewee.Model):
    class Meta:
        database = prod_database_controller.database


class Migration(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField()

    class Meta:
        db_table = "Migrations"


class BalanceOperation(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    recipient_id = peewee.CharField(max_length=28, null=True)
    status = peewee.CharField()
    amount = peewee.IntegerField()
    fee = peewee.IntegerField()
    object_type = peewee.CharField()
    object_id = peewee.CharField(max_length=28)
    created_at = DateTimeTZField()

    class Meta:
        db_table = "BalanceOperations"
        indexes = (
            (("recipient_id",), False),
            (("status",), False),
            (("object_type", "object_id"), False)
        )


class Payable(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    status = peewee.CharField()
    amount = peewee.IntegerField()
    fee = peewee.IntegerField()
    anticipation_fee = peewee.IntegerField()
    fraud_coverage_fee = peewee.IntegerField()
    installment = peewee.IntegerField(null=True)
    payment_date = DateTimeTZField()
    original_payment_date = DateTimeTZField(null=True)
    type = peewee.CharField()
    payment_method = peewee.CharField()
    recipient_id = peewee.CharField(max_length=28)
    split_rule_id = peewee.CharField(max_length=28, null=True)
    created_at = DateTimeTZField()
    accrual_date = DateTimeTZField(null=True)
    transaction_id = peewee.IntegerField()
    bulk_anticipation_id = peewee.CharField(max_length=28, null=True)

    class Meta:
        db_table = "Payables"
        indexes = (
            (("status",), False),
            (("payment_date",), False),
            (("type",), False),
            (("payment_method",), False),
            (("recipient_id",), False),
            (("split_rule_id",), False),
            (("transaction_id",), False),
            (("bulk_anticipation_id",), False)
        )


class Transfer(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    status = peewee.CharField()
    amount = peewee.IntegerField()
    fee = peewee.IntegerField()
    type = peewee.CharField()
    transaction_id = peewee.IntegerField(null=True)
    recipient_id = peewee.CharField(max_length=28, null=True)
    created_at = DateTimeTZField()
    source_type = peewee.CharField()
    source_id = peewee.CharField(max_length=28)
    target_type = peewee.CharField()
    target_id = peewee.CharField(max_length=28)
    metadata = BinaryJSONField(null=True, default={})

    class Meta:
        db_table = "Transfers"
        indexes = (
            (("status",), False),
            (("recipient_id",), False),
            (("type",), False)
        )


class BankAccount(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    bank_code = peewee.CharField(max_length=5)
    agencia = peewee.CharField(max_length=5)
    agencia_dv = peewee.CharField(null=True, max_length=2)
    conta = peewee.CharField(max_length=20)
    conta_dv = peewee.CharField(null=True, max_length=2)
    type = peewee.CharField()
    document_type = peewee.CharField()
    document_number = peewee.CharField(max_length=14)
    legal_name = peewee.CharField()
    charge_transfer_fees = peewee.BooleanField()
    created_at = DateTimeTZField()

    class Meta:
        db_table = "BankAccounts"


class FeeCollection(BaseModel):
    id = peewee.CharField(primary_key=True, max_length=28)
    status = peewee.CharField()
    type = peewee.CharField()
    description = peewee.CharField()
    payment_date = DateTimeTZField()
    amount = peewee.IntegerField()
    object_type = peewee.CharField(null=True)
    object_id = peewee.CharField(max_length=28, null=True)
    recipient_id = peewee.CharField(max_length=28)
    created_at = DateTimeTZField()

    class Meta:
        db_table = "FeeCollections"


class Invoice(BaseModel):
    id = peewee.CharField(primary_key=True, max_length=28)
    serial_number = peewee.IntegerField()
    amount = peewee.IntegerField()
    status = peewee.CharField()
    payment_method = peewee.CharField()
    type = peewee.CharField()
    period_start_date = DateTimeTZField()
    period_end_date = DateTimeTZField()
    metadata = BinaryJSONField()

    class Meta:
        db_table = "Invoices"


class Recipient(BaseModel):
    id = peewee.CharField(primary_key=True, max_length=28)
    transfer_enabled = peewee.BooleanField()
    last_transfer = DateTimeTZField(null=True)
    transfer_interval = peewee.CharField(null=True)
    transfer_day = peewee.IntegerField(null=True)
    automatic_anticipation_enabled = peewee.BooleanField()
    automatic_anticipation_type = peewee.CharField()
    automatic_anticipation_days = peewee.CharField(null=True)
    automatic_anticipation_1025_delay = peewee.IntegerField()
    anticipatable_volume_percentage = peewee.IntegerField(null=True)
    created_at = DateTimeTZField()
    updated_at = DateTimeTZField()
    postback_url = peewee.CharField(null=True)
    status = peewee.CharField()
    status_reason = peewee.CharField(null=True)
    bank_account_id = peewee.IntegerField()

    class Meta:
        db_table = "Recipients"
        indexes = ((("bank_account_id",), False),)


class BulkAnticipation(BaseModel):
    id = peewee.CharField(primary_key=True, max_length=28)
    type = peewee.CharField()
    amount = peewee.IntegerField()
    fee = peewee.IntegerField()
    anticipation_fee = peewee.IntegerField()
    fraud_coverage_fee = peewee.IntegerField(null=True)
    timeframe = peewee.CharField(null=True)
    status = peewee.CharField()
    recipient_id = peewee.CharField(max_length=28)
    created_at = DateTimeTZField()
    updated_at = DateTimeTZField()
    payment_date = DateTimeTZField()

    ENDPOINT = "/recipients/{recipient_id}/bulk_anticipations"

    class Meta:
        db_table = "BulkAnticipations"
        indexes = (
            (("recipient_id",), False),
            (("status",), False)
        )


class Transaction(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    subscription_id = peewee.IntegerField(null=True)
    customer_id = peewee.IntegerField(null=True)
    address_id = peewee.IntegerField(null=True)
    phone_id = peewee.IntegerField(null=True)
    billing_id = peewee.IntegerField(null=True)
    card_id = peewee.CharField(max_length=30)
    status = peewee.CharField()
    status_reason = peewee.CharField()
    acquirer_response_code = peewee.CharField(null=True)
    acquirer_name = peewee.CharField(null=True)
    acquirer_id = peewee.CharField(null=True, max_length=24)
    authorization_code = peewee.CharField(null=True)
    soft_descriptor = peewee.CharField(null=True)
    tid = peewee.CharField(null=True)
    nsu = peewee.CharField(null=True)
    created_at = DateTimeTZField()
    updated_at = DateTimeTZField()
    amount = peewee.IntegerField()
    authorized_amount = peewee.IntegerField()
    paid_amount = peewee.IntegerField()
    refunded_amount = peewee.IntegerField()
    installments = peewee.IntegerField()
    cost = peewee.DoubleField()
    card_holder_name = peewee.CharField(null=True)
    card_last_digits = peewee.CharField(max_length=4)
    card_first_digits = peewee.CharField(max_length=6)
    card_brand = peewee.CharField(null=True)
    card_pin_mode = peewee.CharField(null=True)
    postback_url = peewee.CharField(null=True)
    payment_method = peewee.CharField()
    capture_method = peewee.CharField()
    antifraud_metadata = BinaryJSONField(null=True)
    antifraud_score = peewee.DoubleField(null=True)
    boleto_url = peewee.CharField(null=True)
    boleto_barcode = peewee.CharField(null=True)
    boleto_expiration_date = DateTimeTZField(null=True)
    referer = peewee.CharField(null=True)
    ip = peewee.CharField(null=True)
    reference_key = peewee.CharField(null=True)
    metadata = peewee.CharField(null=True)

    class Meta:
        db_table = "Transactions"
        indexes = (
            (("subscription_id",), False),
            (("customer_id",), False),
            (("address_id",), False),
            (("phone_id",), False),
            (("billing_id",), False),
            (("card_id",), False),
            (("capture_method",), False),
            (("payment_method",), False),
            (("status",), False),
            (("tid",), False)
        )


class Customer(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(null=True)
    email = peewee.CharField(null=True)
    gender = peewee.CharField(null=True)
    document_type = peewee.CharField(null=True)
    document_number = peewee.CharField(null=True)
    born_at = DateTimeTZField(null=True)
    created_at = DateTimeTZField()

    class Meta:
        db_table = "Customers"
        indexes = (
            (("email",), False),
            (("document_type", "document_number"), False)
        )


class Address(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    street = peewee.CharField(null=True)
    street_number = peewee.CharField(null=True)
    complementary = peewee.CharField(null=True)
    neighborhood = peewee.CharField(null=True)
    city = peewee.CharField(null=True)
    state = peewee.CharField(null=True)
    zipcode = peewee.CharField(null=True)
    country = peewee.CharField(null=True)

    class Meta:
        db_table = "Addresses"


class Phone(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    ddi = peewee.CharField(max_length=3)
    ddd = peewee.CharField(null=True)
    number = peewee.CharField(null=True)

    class Meta:
        db_table = "Phones"


class Card(BaseModel):
    id = peewee.CharField(primary_key=True, max_length=30)
    created_at = DateTimeTZField()
    updated_at = DateTimeTZField()
    brand = peewee.CharField(null=True)
    holder_name = peewee.CharField(null=True)
    first_digits = peewee.CharField(null=True, max_length=6)
    last_digits = peewee.CharField(null=True, max_length=4)
    country = peewee.CharField(null=True)
    fingerprint = peewee.CharField(null=True, max_length=40)
    valid = peewee.BooleanField(null=True)
    expiration_date = peewee.CharField(null=True, max_length=7)

    class Meta:
        db_table = "Cards"
        indexes = (
            (("brand",), False),
            (("first_digits",), False),
            (("last_digits",), False),
            (("country",), False),
            (("fingerprint",), False),
            (("first_digits", "last_digits"), False)
        )


class SplitRule(BaseModel):
    id = peewee.CharField(primary_key=True, max_length=28)
    amount = peewee.IntegerField(null=True)
    percentage = peewee.DoubleField(null=True)
    recipient_id = peewee.CharField(max_length=28)
    charge_processing_fee = peewee.BooleanField()
    charge_remainder = peewee.BooleanField(null=True)
    liable = peewee.BooleanField()
    created_at = DateTimeTZField()
    updated_at = DateTimeTZField()

    class Meta:
        db_table = "SplitRules"
        indexes = ((("recipient_id",), False),)


def apply():
    tables = [
        Migration,
        BalanceOperation,
        Payable,
        Transfer,
        BankAccount,
        FeeCollection,
        Invoice,
        Recipient,
        BulkAnticipation,
        Transaction,
        Customer,
        Address,
        Phone,
        Card,
        SplitRule
    ]
    prod_database_controller.database.create_tables(tables)
