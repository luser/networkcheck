#!/usr/bin/env python

import json
import os
import web

from networkcheck import check, hosts
from signalstrength import get_signal_strength

class index:
    def GET(self):
        data = open(os.path.join(os.path.dirname(__file__), 'index.html'), 'rb').read()
        hosttable = '\n'.join('<tr id="%s"><td>%s</td><td class="UNKNOWN">?</td></tr>' % h for h in hosts())
        return data % hosttable

class netdata:
    def GET(self):
        return json.dumps({'hosts': list(check())})

class wifisignal:
    def GET(self):
        s = get_signal_strength('192.168.1.200')
        return json.dumps({'signal': s})

urls = (
    '/', index,
    '/data', netdata,
    '/wifisignal', wifisignal,
)

app = web.application(urls, globals())
application = app.wsgifunc()
