#!/usr/bin/env python

import json
import os
import shutil
import SocketServer

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from networkcheck import check

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/script.js', '/data'):
            self.send_error(404, 'Not Found')
            return
        self.send_response(200)
        self.end_headers()
        if self.path == '/':
            shutil.copyfileobj(open(os.path.join(os.path.dirname(__file__), 'index.html'), 'rb'), self.wfile)
        elif self.path == '/script.js':
            shutil.copyfileobj(open(os.path.join(os.path.dirname(__file__), 'script.js'), 'rb'), self.wfile)
        else:
            self.send_net_data()

    def send_net_data(self):
        self.wfile.write(json.dumps({'hosts': list(check())}))


if __name__ == '__main__':
    Handler = MyRequestHandler
    httpd = HTTPServer(("", 10000), Handler)
    print 'http://%s:%d/' % (httpd.server_name, httpd.server_port)
    httpd.serve_forever()
