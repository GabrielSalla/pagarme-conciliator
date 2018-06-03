import datetime
import pytz
import re


def now():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)


def now_br():
    return now().astimezone(pytz.timezone("America/Sao_Paulo"))


def from_iso(timestamp):
    if timestamp is None:
        return None
    timestamp = re.sub("[:.]", "", timestamp)
    timestamp = re.sub("Z", "+0000", timestamp)
    return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H%M%S%f%z")
