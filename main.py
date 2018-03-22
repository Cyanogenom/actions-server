import data_store
import config, json, logging
from datetime import datetime
from uuid import uuid4

try:
    from SocketServer import ThreadingMixIn
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from socketserver import ThreadingMixIn
    from http.server import HTTPServer, BaseHTTPRequestHandler


class ActionsServer(BaseHTTPRequestHandler):

    _client = None

    def do_GET(self):
        code = 200
        message = 'ok'
        _xid = self.headers['X-Request-Id']

        if config._get_data_url.findall(self.path):
            print(self.path)
            print(self._client)
            print(config.get_min_values.findall(self.path))
            print(config.get_max_values.findall(self.path))

            min_v = config.get_min_values.findall(self.path)
            max_v = config.get_max_values.findall(self.path)
            if len(min_v) == 1 and len(max_v) == 1:
                min_v = float(min_v[0])
                max_v = float(max_v[0])
                try:
                    message = json.dumps({'data': data_store.get_data(self._client, min_v, max_v)})
                except Exception as error:
                    code = 500
                    message = 'Error'
                    _logging(error, _xid)
            else:
                code = 400
                message = "Неверное число параметров."

        elif not config._health_check_url.findall(self.path):
            code = 404
            message = 'Error'

        self.send_response(code)
        self.send_header('Content-Type', 'application/json' if code == 200
                                          else 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode())

    def do_POST(self):
        _xid = self.headers['X-Request-Id']

        code = 200
        if config.send_data_url.findall(self.path):
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))

            try:
                data_store.set_data(self._client, json.dumps(post_data))
            except Exception as error:
                _logging(error, _xid)
            else:
                self.send_response(code)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class Main:
    def __init__(self):
        ActionsServer._client = data_store.create_client(config.project_id)
        serv = ThreadingHTTPServer((config.LISTEN_IP, int(config.LISTEN_PORT)), ActionsServer)

        serv.serve_forever()

def _logging(error, xrid=None, extra=''):
    mess = """{
        "logtime": "%s",
        "loglevel": "%s",
        "logger": "logging",
        "request_id": "%s", 
        "logmsg": "%s"
        "extra": "%s"
    }""" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'), 'Error', uuid4() if xrid is None else xrid, error, extra)

    logging.error(mess)

if __name__ == '__main__':
    m = Main()
