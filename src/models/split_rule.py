from src.models.base import BaseModel
import src.utils.time as time_utils
from playhouse.postgres_ext import DateTimeTZField
import peewee


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

    @classmethod
    def format_from_response(cls, data):
        created_at = time_utils.from_iso(data["date_created"])
        updated_at = time_utils.from_iso(data["date_updated"])

        return dict(
            id=data["id"],
            amount=data["amount"],
            percentage=data["percentage"],
            recipient_id=data["recipient_id"],
            charge_processing_fee=data["charge_processing_fee"],
            charge_remainder=data["charge_remainder"],
            liable=data["liable"],
            created_at=created_at,
            updated_at=updated_at
        )
