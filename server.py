#!/usr/bin/env python

import json
import os
import web

from networkcheck import check, hosts

class index:
    def GET(self):
        data = open(os.path.join(os.path.dirname(__file__), 'index.html'), 'rb').read()
        hosttable = '\n'.join('<tr id="%s"><td>%s</td><td class="UNKNOWN">?</td></tr>' % h for h in hosts())
        return data % hosttable

class netdata:
    def GET(self):
        return json.dumps({'hosts': list(check())})

urls = (
    '/', index,
    '/data', netdata,
)

app = web.application(urls, globals())
application = app.wsgifunc()
