#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import codecs
import json
import os
import web

from networkcheck import check
from signalstrength import get_signal_strength

import config


def format_host(host, name):
    if host == '8.8.8.8':
        maybe_link = name
    else:
        maybe_link = '<a href="https://{host}/">{name}</a>'.format(host=host, name=name)
    return '<tr id="{host}"><td>{name}</td><td class="UNKNOWN">?</td></tr>'.format(
        host=host, name=maybe_link
    )


class index:
    def GET(self):
        data = codecs.open(os.path.join(os.path.dirname(__file__), 'index.html'),
                           'rb', 'utf-8').read()
        hosttable = '\n'.join(format_host(host, name)
                              for (host, name) in config.HOSTS)
        wifi_hosttable = '\n'.join(
            '''<tr><td>{name}</td>
<td><span id="wifisignalvalue_{host}"></span></td></tr>
<tr><td colspan="2">
<meter id="wifisignal_{host}" min="-90" max="-60" low="-78" high="-72" optimum="-65"></meter>
</td></tr>
'''.format(name=name, host=host)

            for (host, name) in config.WIFI_HOSTS
        )
        return data.format(hosts=hosttable, wifi_hosts=wifi_hosttable)


class netdata:
    def GET(self):
        return json.dumps({'hosts': list(check())})


def check_wifi_signal():
    for (host, name) in config.WIFI_HOSTS:
        yield {'host': host, 'signal': get_signal_strength(host)}


class wifisignal:
    def GET(self):
        return json.dumps({'hosts': list(check_wifi_signal())})


class static:
    def GET(self, filename, _):
        raise web.seeother('/static/' + filename)


urls = (
    '/', index,
    '/data', netdata,
    '/wifisignal', wifisignal,
    '/(.+\.(js|css))', static,
)

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
