from src.models.base import BaseModel
import peewee


class Migration(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField()

    class Meta:
        db_table = "Migrations"
