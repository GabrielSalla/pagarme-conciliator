from src.models.base import BaseModel
from src.models.payable import Payable
from src.models.invoice import Invoice
import src.utils.time as time_utils
from playhouse.postgres_ext import BinaryJSONField, DateTimeTZField
import peewee


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

    @classmethod
    def format_from_response(cls, data):
        return dict(
            id=data["id"],
            status=data["status"],
            type=data["type"],
            description=data["description"],
            payment_date=time_utils.from_iso(data["payment_date"]),
            amount=data["amount"],
            object_type=data["object_type"],
            object_id=data["object_id"],
            recipient_id=data["recipient_id"],
            created_at=time_utils.from_iso(data["date_created"])
        )
