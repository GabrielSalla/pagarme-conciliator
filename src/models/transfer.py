from src.models.base import BaseModel
import src.utils.time as time_utils
from playhouse.postgres_ext import BinaryJSONField, DateTimeTZField
import peewee


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

    @classmethod
    def format_from_response(cls, data):
        return dict(
            id=data["id"],
            status=data["status"],
            amount=data["amount"],
            fee=data["fee"],
            type=data["type"],
            transaction_id=data["transaction_id"],
            recipient_id=data["source_id"],
            created_at=time_utils.from_iso(data["date_created"]),
            source_type=data["source_type"],
            source_id=data["source_id"],
            target_type=data["target_type"],
            target_id=data["target_id"],
            metadata=data["metadata"],
            bank_account=data["bank_account"]
        )
