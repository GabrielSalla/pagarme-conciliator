from src.models.base import BaseModel
from playhouse.postgres_ext import BinaryJSONField, DateTimeTZField
import src.utils.time as time_utils
import peewee


def extract_id(data, key):
    try:
        obj = data[key]
        if obj is not None:
            return obj["id"]
        else:
            return None
    except KeyError:
        return None


class Transaction(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    subscription_id = peewee.IntegerField(null=True)
    customer_id = peewee.IntegerField(null=True)
    address_id = peewee.IntegerField(null=True)
    phone_id = peewee.IntegerField(null=True)
    billing_id = peewee.IntegerField(null=True)
    card_id = peewee.CharField(max_length=30)
    status = peewee.CharField()
    status_reason = peewee.CharField()
    acquirer_response_code = peewee.CharField(null=True)
    acquirer_name = peewee.CharField(null=True)
    acquirer_id = peewee.CharField(null=True, max_length=24)
    authorization_code = peewee.CharField(null=True)
    soft_descriptor = peewee.CharField(null=True)
    tid = peewee.CharField(null=True)
    nsu = peewee.CharField(null=True)
    created_at = DateTimeTZField()
    updated_at = DateTimeTZField()
    amount = peewee.IntegerField()
    authorized_amount = peewee.IntegerField()
    paid_amount = peewee.IntegerField()
    refunded_amount = peewee.IntegerField()
    installments = peewee.IntegerField()
    cost = peewee.DoubleField()
    card_holder_name = peewee.CharField(null=True)
    card_last_digits = peewee.CharField(max_length=4)
    card_first_digits = peewee.CharField(max_length=6)
    card_brand = peewee.CharField(null=True)
    card_pin_mode = peewee.CharField(null=True)
    postback_url = peewee.CharField(null=True)
    payment_method = peewee.CharField()
    capture_method = peewee.CharField()
    antifraud_metadata = BinaryJSONField(null=True)
    antifraud_score = peewee.DoubleField(null=True)
    boleto_url = peewee.CharField(null=True)
    boleto_barcode = peewee.CharField(null=True)
    boleto_expiration_date = DateTimeTZField(null=True)
    referer = peewee.CharField(null=True)
    ip = peewee.CharField(null=True)
    reference_key = peewee.CharField(null=True)
    metadata = peewee.CharField(null=True)

    ENDPOINT = "/transactions"

    class Meta:
        db_table = "Transactions"

    @classmethod
    def format_from_response(cls, data):
        customer_id = extract_id(data, "customer")
        address_id = extract_id(data, "address")
        phone_id = extract_id(data, "phone")
        billing_id = extract_id(data, "billing")
        card_id = extract_id(data, "card")

        created_at = time_utils.from_iso(data["date_created"])
        updated_at = time_utils.from_iso(data["date_updated"])
        if data["boleto_expiration_date"] is not None:
            boleto_expiration_date = time_utils.from_iso(
                data["boleto_expiration_date"])
        else:
            boleto_expiration_date = None

        # Missing fields
        try:
            reference_key = data["reference_key"]
        except KeyError:
            reference_key = None
        try:
            acquirer_id = data["acquirer_id"]
        except KeyError:
            acquirer_id = None
        try:
            card_pin_mode = data["card_pin_mode"]
        except KeyError:
            card_pin_mode = None

        return dict(
            id=data["id"],
            subscription_id=data["subscription_id"],
            customer_id=customer_id,
            address_id=address_id,
            phone_id=phone_id,
            billing_id=billing_id,
            card_id=card_id,
            status=data["status"],
            status_reason=data["status_reason"],
            acquirer_response_code=data["acquirer_response_code"],
            acquirer_name=data["acquirer_name"],
            acquirer_id=acquirer_id,
            authorization_code=data["authorization_code"],
            soft_descriptor=data["soft_descriptor"],
            tid=data["tid"],
            nsu=data["nsu"],
            created_at=created_at,
            updated_at=updated_at,
            amount=data["amount"],
            authorized_amount=data["authorized_amount"],
            paid_amount=data["paid_amount"],
            refunded_amount=data["refunded_amount"],
            installments=data["installments"],
            cost=data["cost"],
            card_holder_name=data["card_holder_name"],
            card_last_digits=data["card_last_digits"],
            card_first_digits=data["card_first_digits"],
            card_brand=data["card_brand"],
            card_pin_mode=card_pin_mode,
            postback_url=data["postback_url"],
            payment_method=data["payment_method"],
            capture_method=data["capture_method"],
            antifraud_metadata=data["antifraud_metadata"],
            antifraud_score=data["antifraud_score"],
            boleto_url=data["boleto_url"],
            boleto_barcode=data["boleto_barcode"],
            boleto_expiration_date=boleto_expiration_date,
            referer=data["referer"],
            ip=data["ip"],
            reference_key=reference_key,
            metadata=data["metadata"]
        )
