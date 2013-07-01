"""
Model for scramble api.
"""
from sqlalchemy import MetaData, Column
from sqlalchemy.sql import and_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, DateTime, Text, Unicode, Integer
from pytz import utc

from .dateutils import from_seconds_string, to_seconds_string


DBSession = scoped_session(sessionmaker(autoflush=False, autocommit=False))


metadata = MetaData()


Base = declarative_base(metadata=metadata)


def init_model(engine):
    DBSession.bind = engine
    metadata.bind = engine


class UTCDateTime(TypeDecorator):
    """
    DateTime type that confirms that a datetime is UTC when entering and
    exiting the database.
    """

    impl = DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            assert value.tzinfo == utc
        return value

    def process_result_value(self, value, engine):
        if value is not None:
            if not value.tzinfo:
                value = value.astimezone(utc)
            elif value.tzinfo != utc:
                value = value.astimezone(utc)
            return value


class Event(Base):

    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title =  Column(Unicode(), nullable=False)
    description =  Column(Text(), nullable=False)
    start_date = Column(UTCDateTime(timezone=True), nullable=False)
    end_date = Column(UTCDateTime(timezone=True), nullable=True)

    def __init__(self, title, description, start_date, end_date=None, id_=None):
        self.title = title
        self.description = description
        self.start_date = start_date
        if end_date:
            self.end_date = end_date
        if id_:
            self.id = id_

    def to_dict(self):
        """ Convert an event model into a regular dictionary. """
        d = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'startDate': to_seconds_string(self.start_date),
        }
        if self.end_date:
            d['endDate'] = to_seconds_string(self.end_date)
        return d

    @staticmethod
    def from_dict(d):
        """ Create an event model from a regular dictionary.

        @NOTE: This does not do input validation.
        """
        start_date = from_seconds_string(d['startDate'])
        if 'endDate' in d:
            end_date = from_seconds_string(d['endDate'])
        else:
            end_date = None
        return Event(d['title'], d['description'], start_date,
            end_date=end_date)

    @staticmethod
    def get_event(event_id):
        """ Get a single event with the given id. """
        try:
            event_id = int(event_id)
        except ValueError:
            event_id = None
        except TypeError:
            event_id = None
        if event_id:
            return DBSession.query(Event).filter(Event.id == event_id).first()
        else:
            return None

    @staticmethod
    def get_events(starts_on_or_after_date=None, starts_before_date=None,
        limit=20, offset=0):
        """ Get a list of events with the given conditions. """
        and_args = []
        if starts_on_or_after_date:
            and_args.append(Event.start_date >= starts_on_or_after_date)
        if starts_before_date:
            and_args.append(Event.start_date < starts_before_date)
        query = DBSession.query(Event).filter(and_(*and_args))
        query = query.order_by(Event.start_date)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query.all()
