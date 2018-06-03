from src.models.base import BaseModel
from playhouse.postgres_ext import DateTimeTZField
import src.utils.time as time_utils
import peewee


class BalanceOperation(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    recipient_id = peewee.CharField(max_length=28, null=True)
    status = peewee.CharField()
    amount = peewee.IntegerField()
    fee = peewee.IntegerField()
    object_type = peewee.CharField()
    object_id = peewee.CharField(max_length=28)
    created_at = DateTimeTZField()

    ENDPOINT = "/balance/operations"

    class Meta:
        db_table = "BalanceOperations"

    @classmethod
    def format_from_response(cls, data):
        movement_object = data["movement_object"]
        if movement_object["object"] in ["payable", "fee_collection"]:
            recipient_id = movement_object["recipient_id"]
        elif movement_object["object"] == "transfer":
            recipient_id = movement_object["source_id"]

        return dict(
            id=data["id"],
            recipient_id=recipient_id,
            status=data["status"],
            amount=data["amount"],
            fee=data["fee"],
            object_type=data["type"],
            object_id=data["movement_object"]["id"],
            created_at=time_utils.from_iso(data["date_created"])
        )
