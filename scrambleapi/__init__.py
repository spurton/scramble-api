from pyramid.config import Configurator
from pyramid.events import NewRequest
from sqlalchemy import engine_from_config

from .model import init_model, DBSession


def remove_session_callback(event):
    # Clean up the sqlalchemy session after each request.
    DBSession.remove()


def main(global_config, **settings):
    engine = engine_from_config(settings, prefix="sqlalchemy.")
    init_model(engine)

    config = Configurator(settings=settings)
    config.add_subscriber(remove_session_callback, NewRequest)
    config.scan()

    return config.make_wsgi_app()
