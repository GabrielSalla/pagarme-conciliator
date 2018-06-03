from src.models.base import BaseModel
import src.utils.time as time_utils
from playhouse.postgres_ext import DateTimeTZField
import peewee


class BankAccount(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    bank_code = peewee.CharField(max_length=5)
    agencia = peewee.CharField(max_length=5)
    agencia_dv = peewee.CharField(null=True, max_length=20)
    conta = peewee.CharField(max_length=10)
    conta_dv = peewee.CharField(null=True, max_length=20)
    type = peewee.CharField()
    document_type = peewee.CharField()
    document_number = peewee.CharField(max_length=14)
    legal_name = peewee.CharField()
    charge_transfer_fees = peewee.BooleanField()
    created_at = DateTimeTZField()

    class Meta:
        db_table = "BankAccounts"

    @classmethod
    def format_from_response(cls, data):
        return dict(
            id=data["id"],
            bank_code=data["bank_code"],
            agencia=data["agencia"],
            agencia_dv=data["agencia_dv"],
            conta=data["conta"],
            conta_dv=data["conta_dv"],
            type=data["type"],
            document_type=data["document_type"],
            document_number=data["document_number"],
            legal_name=data["legal_name"],
            charge_transfer_fees=data["charge_transfer_fees"],
            created_at=time_utils.from_iso(data["date_created"])
        )
