from datetime import datetime
from pytz import utc


date_format = "%Y-%m-%d %H:%M:%S %Z%z"


seconds_format = "%s"


def utc_now():
    return datetime.now(tz=utc)


def to_seconds_string(when):
    return when.strftime(seconds_format)


def from_seconds_string(date_string):
    timestamp = long(date_string)
    return datetime.utcfromtimestamp(timestamp).replace(tzinfo=utc)
