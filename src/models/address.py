from src.models.base import BaseModel
import peewee


class Address(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    street = peewee.CharField(null=True)
    street_number = peewee.CharField(null=True)
    complementary = peewee.CharField(null=True)
    neighborhood = peewee.CharField(null=True)
    city = peewee.CharField(null=True)
    state = peewee.CharField(null=True)
    zipcode = peewee.CharField(null=True)
    country = peewee.CharField(null=True)

    class Meta:
        db_table = "Addresses"

    @classmethod
    def format_from_response(cls, data):
        return dict(
            id=data["id"],
            street=data["street"],
            complementary=data["complementary"],
            street_number=data["street_number"],
            neighborhood=data["neighborhood"],
            city=data["city"],
            state=data["state"],
            zipcode=data["zipcode"],
            country=data["country"]
        )
