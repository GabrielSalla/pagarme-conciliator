from src.models.base import BaseModel
from playhouse.postgres_ext import DateTimeTZField
import src.utils.time as time_utils
import peewee


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

    @classmethod
    def format_from_response(cls, data):
        return dict(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            gender=data["gender"],
            document_type=data["document_type"],
            document_number=data["document_number"],
            born_at=time_utils.from_iso(data["born_at"]),
            created_at=time_utils.from_iso(data["date_created"])
        )
