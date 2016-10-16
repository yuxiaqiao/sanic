import ujson

STATUS_CODES = {
    200: b'OK',
    400: b'Bad Request',
    401: b'Unauthorized',
    402: b'Payment Required',
    403: b'Forbidden',
    404: b'Not Found',
    405: b'Method Not Allowed',
    500: b'Internal Server Error',
    501: b'Not Implemented',
    502: b'Bad Gateway',
    503: b'Service Unavailable',
    504: b'Gateway Timeout',
}
from sanic.log import log
class HTTPResponse:
    __slots__ = ('body', 'status', 'content_type', 'headers')

    def __init__(self, status=200, headers=None, body=None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    def output(self, version="1.1", keep_alive=False, keep_alive_timeout=None):
        # This is all returned in a kind-of funky way
        # We tried to make this as fast as possible in pure python

        timeout_header = b''
        if keep_alive and keep_alive_timeout:
            timeout_header = b'Keep-Alive: timeout=%d\r\n' % keep_alive_timeout

        headers = b''

        if self.headers:
            headers = b''.join(
                b'%b: %b\r\n' % (name.encode(), value.encode('utf-8')) for name, value in self.headers.items())

        return b'HTTP/%b %d %b\r\nContent-Length: %d\r\nConnection: %b\r\n%b%b\r\n%b' % (
                        version.encode(),
                        self.status,
                        STATUS_CODES.get(self.status, b'FAIL'),
                        len(self.body),
                        b'keep-alive' if keep_alive else b'close',
                        timeout_header,
                        headers,
                        self.body
            )

    def json(self, body):
        self.headers['Content-Type'] = "application/json; charset=utf-8"
        self.body = ujson.dumps(body).encode('utf-8')
        return self

    def text(self, body):
        self.headers['Content-Type'] = "text/plain; charset=utf-8"
        self.body = body.encode('utf-8')
        return self

    def html(self, body):
        self.headers['Content-Type'] = "text/html; charset=utf-8"
        self.body = body.encode('utf-8')
        return self