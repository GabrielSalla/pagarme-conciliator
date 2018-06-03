from src.models.base import BaseModel
from playhouse.postgres_ext import DateTimeTZField
import src.utils.time as time_utils
import peewee


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

    @classmethod
    def format_from_response(cls, data):
        try:
            fraud_coverage_fee = data["fraud_coverage_fee"]
        except KeyError:
            fraud_coverage_fee = None

        created_at = time_utils.from_iso(data["date_created"])
        updated_at = time_utils.from_iso(data["date_updated"])
        payment_date = time_utils.from_iso(data["payment_date"])

        return dict(
            id=data["id"],
            type=data["type"],
            amount=data["amount"],
            fee=data["fee"],
            anticipation_fee=data["anticipation_fee"],
            fraud_coverage_fee=fraud_coverage_fee,
            timeframe=data["timeframe"],
            status=data["status"],
            recipient_id=data["recipient_id"],
            created_at=created_at,
            updated_at=updated_at,
            payment_date=payment_date
        )
