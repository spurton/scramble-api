import logging

from cornice import Service
from pytz import utc

from .utils import _401, _404
from .model import DBSession, Event
from .dateutils import from_seconds_string


log = logging.getLogger(__name__)


events_service = Service(name="events_service", path="/events",
    description="Create an event, delete an event or fetch a list of events.")


event_service = Service(name="event_service", path="/events/{event_id}",
    description="Get an event.")


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
    filter_kwargs = {}
    # @TODO: Validation.
    if request.GET.get('starts_on_or_after_date', None):
        filter_kwargs['starts_on_or_after_date'] = \
            from_seconds_string(request.GET['starts_on_or_after_date'])
    # @TODO: Validation.
    if request.GET.get('starts_before_date', None):
        filter_kwargs['starts_before_date'] = from_seconds_string(request.GET['starts_before_date'])
    # @TODO: Validation.
    if request.GET.get('limit', None):
        filter_kwargs['limit'] = int(request.GET['limit'])
    # @TODO: Validation.
    if request.GET.get('offset', None):
        filter_kwargs['offset'] = int(request.GET['offset'])
    print filter_kwargs
    return {
        'events': [
            event.id for event in Event.get_events(**filter_kwargs)
        ]
    }


@event_service.get()
def get_event(request):
    event = Event.get_event(request.matchdict['event_id'])
    if not event:
        raise _404()
    return event.to_dict()


@event_service.delete(validators=check_token)
def delete_event(request):
    event = Event.get_event(request.matchdict['event_id'])
    if not event:
        raise _404()
    DBSession.delete(event)
    DBSession.commit()
    return {}


@events_service.post(validators=check_token)
def create_event(request):
    # @TODO: Validation.
    event = Event.from_dict(request.json_body)
    DBSession.add(event)
    DBSession.commit()
    return event.to_dict()
