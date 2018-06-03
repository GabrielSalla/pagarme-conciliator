from src.models.base import BaseModel
from playhouse.postgres_ext import DateTimeTZField
import src.utils.time as time_utils
import peewee


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

    ENDPOINT = "/recipients"

    class Meta:
        db_table = "Recipients"

    @classmethod
    def format_from_response(cls, data):
        bank_account = data["bank_account"]
        try:
            bank_account_id = bank_account["id"]
        except KeyError:
            bank_account_id = None

        anticipation_enabled = data["automatic_anticipation_enabled"]
        anticipation_type = data["automatic_anticipation_type"]
        anticipation_days = data["automatic_anticipation_days"]
        anticipation_1025_delay = data["automatic_anticipation_1025_delay"]
        volume_percentage = data["anticipatable_volume_percentage"]

        last_transfer = time_utils.from_iso(data["last_transfer"])
        created_at = time_utils.from_iso(data["date_created"])
        updated_at = time_utils.from_iso(data["date_updated"])

        return dict(
            id=data["id"],
            transfer_enabled=data["transfer_enabled"],
            last_transfer=last_transfer,
            transfer_interval=data["transfer_interval"],
            transfer_day=data["transfer_day"],
            automatic_anticipation_enabled=anticipation_enabled,
            automatic_anticipation_type=anticipation_type,
            automatic_anticipation_days=anticipation_days,
            automatic_anticipation_1025_delay=anticipation_1025_delay,
            anticipatable_volume_percentage=volume_percentage,
            created_at=created_at,
            updated_at=updated_at,
            postback_url=data["postback_url"],
            status=data["status"],
            status_reason=data["status_reason"],
            bank_account_id=bank_account_id
        )
