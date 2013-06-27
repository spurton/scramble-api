import logging
from cornice import Service
from pytz import utc
from .utils import _401


log = logging.getLogger(__name__)


events_service = Service(name="events_service", path="/events",
    description="Create an event, delete an event or fetch a list of events.")


event_service = Service(name="event_service", path="/events/{event_id}",
    description="Get an event.")


EVENTS_KEY = "events"


def event_start_date_key(event_id):
    return "event:{0}:startDate".format(event_id)


def event_end_date_key(event_id):
    return "event:{0}:endDate".format(event_id)


def event_title_key(event_id):
    return "event:{0}:title".format(event_id)


def event_description_key(event_id):
    return "event:{0}:description".format(event_id)


TOKEN_HEADER = "X-EVENT-TOKEN"


approved_accounts = {
    "0": {"key": "secret"},
}


def check_token(request):
    token = request.headers.get(TOKEN_HEADER)
    if token is None or '-' not in token:
        raise _401()
    account_id, account_key = token.split('-', 1)
    account = approved_accounts.get(account_id)
    if not account or account['key'] != account_key:
        raise _401()
    request.validated['account'] = account


@events_service.get()
def get_events(request):
    """ Returns a list of all events. """
    return {
        'events': [
            event_id for event_id in request.redis.sort(EVENTS_KEY, by="event:*:startDate")]
    }


@event_service.get()
def get_event(request):
    event = {
        "id": request.matchdict['event_id'],
        "title": request.redis.get(
            event_title_key(request.matchdict['event_id'])),
        "description": request.redis.get(
            event_description_key(request.matchdict['event_id'])),
        "startDate": request.redis.get(
            event_start_date_key(request.matchdict['event_id'])),
    }
    end_date = request.redis.get(
            event_end_date_key(request.matchdict['event_id']))
    if end_date:
        event["endDate"] = end_date
    return event


@event_service.delete(validators=check_token)
def delete_event(request):
    event_id = request.matchdict['event_id']
    request.redis.delete(event_title_key(event_id))
    request.redis.delete(event_description_key(event_id))
    return {}


@events_service.post(validators=check_token)
def create_event(request):
    event_id = request.redis.incr("nextEventId")
    title = request.json_body['title']
    description = request.json_body['description']
    start_date = request.json_body['startDate']
    end_date = request.json_body.get('endDate', None)
    request.redis.set(event_title_key(event_id), title)
    request.redis.set(event_description_key(event_id), description)
    request.redis.set(event_start_date_key(event_id), start_date)
    if end_date:
        request.redis.set(event_end_date_key(event_id), end_date)
    request.redis.lpush(EVENTS_KEY, event_id)
    event = {
        "id": event_id,
        "title": title,
        "description": description,
        "startDate": start_date,
    }
    if end_date:
        event['endDate'] = end_date
    return event
