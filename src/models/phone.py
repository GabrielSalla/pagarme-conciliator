from src.models.base import BaseModel
import peewee


class Phone(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    ddi = peewee.CharField(max_length=3)
    ddd = peewee.CharField(null=True)
    number = peewee.CharField(null=True)

    class Meta:
        db_table = "Phones"

    @classmethod
    def format_from_response(cls, data):
        return dict(
            id=data["id"],
            ddi=data["ddi"],
            ddd=data["ddd"],
            number=data["number"]
        )
