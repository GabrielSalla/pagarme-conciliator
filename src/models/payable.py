from src.models.base import BaseModel
import src.utils.time as time_utils
from playhouse.postgres_ext import DateTimeTZField
import peewee


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

    @classmethod
    def format_from_response(cls, data):
        return dict(
            id=data["id"],
            status=data["status"],
            amount=data["amount"],
            fee=data["fee"],
            anticipation_fee=data["anticipation_fee"],
            fraud_coverage_fee=data["fraud_coverage_fee"],
            installment=data["installment"],
            payment_date=time_utils.from_iso(data["payment_date"]),
            original_payment_date=time_utils.from_iso(
                data["original_payment_date"]),
            type=data["type"],
            payment_method=data["payment_method"],
            recipient_id=data["recipient_id"],
            split_rule_id=data["split_rule_id"],
            created_at=time_utils.from_iso(data["date_created"]),
            accrual_date=time_utils.from_iso(data["accrual_date"]),
            transaction_id=data["transaction_id"],
            bulk_anticipation_id=data["bulk_anticipation_id"]
        )
