from pyramid.config import Configurator
from redis import StrictRedis


def main(global_config, **settings):
    # @TODO: Move this information into the configuration file.
    settings['redis'] = StrictRedis(host='localhost', port=6379, db=0)
    config = Configurator(settings=settings)
    def get_redis(request):
        return request.registry.settings['redis']
    config.add_request_method(get_redis, 'redis', reify=True)
    config.scan()
    return config.make_wsgi_app()
