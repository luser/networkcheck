#!/usr/bin/env python

import json
import os
import shutil
import SocketServer

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from networkcheck import check, hosts

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/script.js', '/style.css', '/data'):
            self.send_error(404, 'Not Found')
            return
        self.send_response(200)
        self.end_headers()
        if self.path == '/':
            self.send_index()
        elif self.path in ('/script.js', '/style.css'):
                           shutil.copyfileobj(open(os.path.join(os.path.dirname(__file__), self.path[1:]), 'rb'), self.wfile)
        else:
            self.send_net_data()

    def send_index(self):
        data = open(os.path.join(os.path.dirname(__file__), 'index.html'), 'rb').read()
        hosttable = '\n'.join('<tr id="%s"><td>%s</td><td class="UNKNOWN">?</td></tr>' % h for h in hosts())
        self.wfile.write(data % hosttable)

    def send_net_data(self):
        self.wfile.write(json.dumps({'hosts': list(check())}))


if __name__ == '__main__':
    Handler = MyRequestHandler
    httpd = HTTPServer(("", 10000), Handler)
    print 'http://%s:%d/' % (httpd.server_name, httpd.server_port)
    httpd.serve_forever()
