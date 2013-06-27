from requests import get, post, delete
from json import dumps as write_json
from pytz import utc
from datetime import datetime, timedelta


uri = "http://localhost:6543"


date_format = "%Y-%m-%d %H:%M:%S %Z%z"


epoch = datetime(1970, 1, 1, tzinfo=utc)


def now():
    return datetime.now(tz=utc)


def seconds_since_epoch(when=None):
    if when is None:
        when = now()
    t = long(round((when - epoch).total_seconds()))
    return t


first_event = {
     "title": "Hack-a-thon",
     "description": "Bakersfield's first hackathon.",
     "startDate": seconds_since_epoch(),
}


# Create an event.
response = post(uri + "/events", data=write_json(first_event), headers={
    "X-EVENT-TOKEN": "0-secret"
})
# Fetch it back.
event = get(uri + "/events/" + str(response.json()['id'])).json()
# Assert the id is in the event id list.
assert event['id'] in get(uri + "/events").json()['events']
print get(uri + "/events").json()['events']
