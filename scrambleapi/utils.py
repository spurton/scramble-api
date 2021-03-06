from webob import Response, exc
from json import dumps as write_json


class _401(exc.HTTPError):
    def __init__(self, msg='Unauthorized'):
        body = {'status': 401, 'message': msg}
        Response.__init__(self, write_json(body))
        self.status = 401
        self.content_type = 'application/json'


class _404(exc.HTTPError):
    def __init__(self, msg='Not Found'):
        body = {'status': 404, 'message': msg}
        Response.__init__(self, write_json(body))
        self.status = 404
        self.content_type = 'application/json'
