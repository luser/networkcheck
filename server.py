#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import codecs
import json
import os
import web

from networkcheck import check, hosts
from signalstrength import get_signal_strength


class index:
    def GET(self):
        data = codecs.open(os.path.join(os.path.dirname(__file__), 'index.html'),
                           'rb', 'utf-8').read()
        hosttable = '\n'.join(
            '<tr id="%s"><td>%s</td><td class="UNKNOWN">?</td></tr>' % h for h in hosts()
        )
        wifi_hosttable = '\n'.join(
            '''<tr><td>%s</td>
<td><span id="wifisignalvalue_%s"></span></td></tr>
<tr><td colspan="2">
<meter id="wifisignal_%s" min="-90" max="-60" low="-78" high="-72" optimum="-65"></meter>
</td></tr>
''' % (name, host, host)

            for (host, name) in wifi_hosts()
        )
        return data.format(hosts=hosttable, wifi_hosts=wifi_hosttable)


class netdata:
    def GET(self):
        return json.dumps({'hosts': list(check())})


def wifi_hosts():
    return [
        ('10.0.1.3', '4955↔4975'),
        ('10.0.0.3', '4975↔5061'),
    ]


def check_wifi_signal():
    for (host, name) in wifi_hosts():
        yield {'host': host, 'signal': get_signal_strength(host)}


class wifisignal:
    def GET(self):
        return json.dumps({'hosts': list(check_wifi_signal())})


urls = (
    '/', index,
    '/data', netdata,
    '/wifisignal', wifisignal,
)

app = web.application(urls, globals())
application = app.wsgifunc()
