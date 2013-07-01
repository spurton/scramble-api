from requests import get, post, delete
from json import dumps as write_json
from pytz import utc
from datetime import datetime, timedelta
from scrambleapi.dateutils import to_seconds_string


uri = "http://localhost:6543"


def utc_now():
    return datetime.now(tz=utc)


first_event = {
     "title": "Hack-a-thon",
     "description": "Bakersfield's first hackathon.",
     "startDate": to_seconds_string(utc_now()),
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
