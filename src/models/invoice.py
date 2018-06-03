from src.models.base import BaseModel
import src.utils.time as time_utils
from playhouse.postgres_ext import BinaryJSONField, DateTimeTZField
import peewee


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

    @classmethod
    def format_from_response(cls, data):
        return dict(
            id=data["id"],
            serial_number=data["serial_number"],
            amount=data["amount"],
            status=data["status"],
            payment_method=data["payment_method"],
            type=data["type"],
            period_start_date=time_utils.from_iso(data["period_start_date"]),
            period_end_date=time_utils.from_iso(data["period_end_date"]),
            metadata=data["metadata"]
        )
