from src.models.base import BaseModel
from playhouse.postgres_ext import DateTimeTZField
import src.utils.time as time_utils
import peewee


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

    @classmethod
    def format_from_response(cls, data):
        created_at = time_utils.from_iso(data["date_created"])
        updated_at = time_utils.from_iso(data["date_updated"])

        return dict(
            id=data["id"],
            created_at=created_at,
            updated_at=updated_at,
            brand=data["brand"],
            holder_name=data["holder_name"],
            first_digits=data["first_digits"],
            last_digits=data["last_digits"],
            country=data["country"],
            fingerprint=data["fingerprint"],
            valid=data["valid"],
            expiration_date=data["expiration_date"]
        )
