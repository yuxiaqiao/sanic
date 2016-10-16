import ujson

STATUS_CODES = {
    200: 'OK',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
}

class HTTPResponse:
    __slots__ = ('body', 'status', 'content_type', 'headers')

    def __init__(self, status=200, headers=None, body=None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    def output(self, version="1.1", keep_alive=False, keep_alive_timeout=None):
        # This is all returned in a kind-of funky way
        # We tried to make this as fast as possible in pure python
        additional_headers = []
        if keep_alive and not keep_alive_timeout is None:
            additional_headers = [b'Keep-Alive: timeout=', str(keep_alive_timeout).encode(), b's\r\n']
        if self.headers:
            for name, value in self.headers.items():
                additional_headers.append('{}: {}\r\n'.format(name, value).encode('utf-8'))

        return b''.join([
                            'HTTP/{} {} {}\r\n'.format(version, self.status,
                                                       STATUS_CODES.get(self.status, 'FAIL')).encode(),
                            b'Content-Type: ', self.headers.get('Content-Type', 'text/plain').encode(), b'\r\n',
                            b'Content-Length: ', str(len(self.body)).encode(), b'\r\n',
                            b'Connection: ', ('keep-alive' if keep_alive else 'close').encode(), b'\r\n',
                        ] + additional_headers + [
                            b'\r\n',
                            self.body or b'',
                        ])

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